from django.test import SimpleTestCase


class ModelFieldDeclarationTestCase(SimpleTestCase):
    """
    A generic test case for testing model field declarations.

    Required attributes are:
    model
    """

    def assertFieldDeclaredAs(self, field_name: str, **kwargs) -> None:
        """
        Fail if any of the attributes on the field given by field_name
        do not match those given.
        """
        field = self.model._meta.get_field(field_name)
        for attribute, expected_value in kwargs.items():
            actual_value = getattr(field, attribute)
            self.assertEqual(
                actual_value,
                expected_value,
                msg=f"{self.model.__name__}.{field_name} has attribute "
                f"{attribute} = {repr(actual_value)}, expected {repr(expected_value)}.",
            )
