import inspect
from typing import Dict, Any, Callable, Type
from pydantic import create_model, ValidationError
from .base import ToolResult

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.schemas: Dict[str, Type] = {}

    def register(self, name: str, func: Callable):
        self.tools[name] = func
        # Create a pydantic model for validation based on function signature
        sig = inspect.signature(func)
        fields = {}
        for param in sig.parameters.values():
            if param.annotation == inspect._empty:
                fields[param.name] = (Any, ...)
            else:
                fields[param.name] = (param.annotation, ... if param.default == inspect._empty else param.default)
        
        self.schemas[name] = create_model(f"{name}_schema", **fields)

    def execute(self, name: str, args: Dict[str, Any]) -> ToolResult:
        if name not in self.tools:
            return ToolResult(success=False, error=f"Tool '{name}' not found.")
        
        # Fuzzy mapping for common argument name hallucinations
        fuzzy_map = {
            "file_path": ["filename", "file_name", "path", "filepath", "folder_path"],
            "folder_path": ["directory", "path", "folder"],
            "content": ["data", "text", "body"]
        }
        
        sig = inspect.signature(self.tools[name])
        target_params = sig.parameters.keys()
        
        fixed_args = args.copy()
        for target, aliases in fuzzy_map.items():
            if target in target_params and target not in fixed_args:
                for alias in aliases:
                    if alias in fixed_args:
                        fixed_args[target] = fixed_args.pop(alias)
                        break

        try:
            # Validate arguments
            validated_args = self.schemas[name](**fixed_args)
            result = self.tools[name](**validated_args.model_dump())
            
            if isinstance(result, ToolResult):
                return result
            return ToolResult(success=True, data=result)
        
        except ValidationError as e:
            return ToolResult(success=False, error=f"Validation Error: {str(e)}")
        except Exception as e:
            return ToolResult(success=False, error=f"Execution Error: {str(e)}")

registry = ToolRegistry()
