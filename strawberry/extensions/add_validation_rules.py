from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, List, Type

from strawberry.extensions.base_extension import SchemaExtension

if TYPE_CHECKING:
    from graphqlx import ASTValidationRule


class AddValidationRules(SchemaExtension):
    """Add graphql-core validation rules.

    Example:
    ```python
    import strawberry
    from strawberry.extensions import AddValidationRules
    from graphqlx import ValidationRule, GraphQLError


    class MyCustomRule(ValidationRule):
        def enter_field(self, node, *args) -> None:
            if node.name.value == "secret_field":
                self.report_error(GraphQLError("Can't query field 'secret_field'"))


    schema = strawberry.Schema(
        Query,
        extensions=[
            AddValidationRules(
                [
                    MyCustomRule,
                ]
            ),
        ],
    )
    ```
    """

    validation_rules: List[Type[ASTValidationRule]]

    def __init__(self, validation_rules: List[Type[ASTValidationRule]]) -> None:
        self.validation_rules = validation_rules

    def on_operation(self) -> Iterator[None]:
        self.execution_context.validation_rules = (
            self.execution_context.validation_rules + tuple(self.validation_rules)
        )
        yield


__all__ = ["AddValidationRules"]
