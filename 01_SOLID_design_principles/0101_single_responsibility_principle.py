"""
Single Responsibility Principle (SRP)
AKA Separation Of Concerns (SOC)

If you have a class, the class should have its primary responsibility and should not take on other responsibilities.
"""

class Journal:
    """
    This class represents a journal for your thoughts
    """
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        """
        This is a dunder method that defines how to print the Journal class object as a string.
        Learn more about dunder methods, __str__ and __repr__ here:
        https://www.digitalocean.com/community/tutorials/python-str-repr-functions
        """
        return "\n".join(self.entries)

    # The following methods break SRP!
    def save(self, filename):
        file = open(filename, "w")
        file.write(str(self))
        file.close()

    def load(self, filename):
        pass

    def load_from_web(self, uri):
        pass
    # We can keep SRP with a separate class for the previous methods

class PersistenceManager:
    """
    This class handles class persistence.
    This is useful to keep SRP.
    """
    @staticmethod
    def save_to_file(journal, filename):
        file = open(filename, "w")
        file.write(str(journal))
        file.close()

j = Journal()
j.add_entry("I cried today.")
j.add_entry("I ate a bug.")
print(f"Journal entries:\n{j}\n")

from pathlib import Path
p = PersistenceManager()
file = str(Path.home() / 'journal.txt')
p.save_to_file(j, file)

# verify that the file was stored correctly
with open(file) as fh:
    print(fh.read())
