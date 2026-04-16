import abc

class BaseParser(abc.ABC):
    @abc.abstractmethod
    def to_markdown(self, filepath: str) -> str:
        """
        Convert a document represented by filepath to Markdown representation.
        Returns the markdown string.
        """
        pass
