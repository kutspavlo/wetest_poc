from poco.exceptions import PocoTargetTimeout


class BasePage:
    """Base class for all Page Objects."""

    def __init__(self, poco):
        self.poco = poco

    def _get_element(self, locator):
        """
        Helper to construct a Poco object from a locator tuple.

        Locator Convention:
        - ("base", "name") -> poco("base").offspring("name")
        - ("base", ">name") -> poco("base").child("name")
        - ("base", "name1", ">name2") -> poco("base").offspring("name1").child("name2")
        - ("base", {"text": "foo"}) -> poco("base").offspring({"text": "foo"})
        """
        if not isinstance(locator, (list, tuple)) or not locator:
            raise ValueError("Locator must be a non-empty tuple or list")

        element = self.poco(locator[0])  # Get the base element

        if len(locator) > 1:
            for part in locator[1:]:  # Loop through the rest of the chain

                # Check if the part is a string and starts with ">"
                if isinstance(part, str) and part.startswith(">"):
                    # It's a child selector
                    child_name = part[1:]  # Get the name after the ">"
                    if not child_name:
                        raise ValueError("Child selector '>' must be followed by a name.")
                    element = element.child(child_name)
                else:
                    # It's an offspring selector (the default)
                    # This also works for non-string locators (e.g., dicts)
                    element = element.offspring(part)

        return element

    def wait_for_element(self, locator, timeout=30):
        """
        Waits for an element to appear.
        Replaces time.sleep() for reliable waiting.
        """
        element = self._get_element(locator)
        element.wait_for_appearance(timeout=timeout)
        return element

    def click_element(self, locator, timeout=30):
        """Waits for an element and then clicks it."""
        element = self.wait_for_element(locator, timeout)
        element.click()
        return element

    def is_element_visible(self, locator, timeout=5):
        """
        Checks if an element exists without failing.
        Returns True or False.
        """
        try:
            # Use a short timeout for existence checks
            self.wait_for_element(locator, timeout=timeout)
            return True
        except PocoTargetTimeout:
            return False