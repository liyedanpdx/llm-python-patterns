# 1. The SOLID Design Principle

## **Snap Step 1 [Single Responsibility Principle (SRP)]**

One of the **SOLID** principles.

> A class, module, or function should have only one reason to change.
> 

It means:

- **Do one thing and do it well**
- Each part of your code should focus on a single responsibility
- Easier to maintain, test, and reuse

**Example**

❌ **Breaking SRP** – *A “Swiss army knife” class that does everything*

```python
class Report:
    def generate(self):
        print("Calculating report data...")
        print("Printing report...")
        print("Saving report to file...")
```

✅ **Following SRP** – *Each class has its own job*

```python
class ReportGenerator:
    def generate(self):
        print("Calculating report data...")

class ReportPrinter:
    def print(self):
        print("Printing report...")

class ReportSaver:
    def save(self):
        print("Saving report to file...")
```

Now if you change how reports are **saved**, you only touch `ReportSaver` — no risk of breaking **generation** or **printing**.

## **Snap Step 2 [Separation of Concerns (SoC)]**

A general software design principle.

> Split a system into distinct parts, each handling a specific concern.
> 

It means:

- **Different concerns = different places in the code**
- Improves clarity, reusability, and maintainability
- Often applied at a **bigger scale** than SRP — SRP is about *one class/module*, SoC is about *system architecture*

## **Snap Step 3 [Python Underscore Naming Conventions]**

| Form | Meaning / Usage |
| --- | --- |
| `__method__` | Python **special (magic/dunder) method**. Called by the interpreter, not usually directly. Examples: `__init__` (constructor), `__str__` (for `print(obj)`), `__len__` (for `len(obj)`). Can be inherited by subclasses; overriding changes built-in behavior. |
| `_method` | **Internal-use convention** (protected-like). Indicates the method/variable is for internal use. Subclasses can access it. No enforcement; external code can still call it. |
| `__method` | Triggers **name mangling**: compiler renames to `_ClassName__method`. Used to avoid accidental override by subclasses (private-like). Can still be accessed externally via `_ClassName__method`, but not recommended. |
| `_` | **Temporary or “ignore” variable**. Often used to indicate a value is unimportant. In interactive shells, `_` holds the last expression’s result. |

✅ **Key Takeaways**:

- Double underscores **before and after** → special system method
- Single leading underscore → internal/protected convention
- Double leading underscore → private, name-mangled
- Single underscore → temporary/ignored value

## **Snap Step 4 [Python `__str__` vs Default Object Representation]**

### Example

```python
class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f'{self.count}: {text}')

    def remove_entry(self, pos):
        del self.entries[pos]

    # Uncomment to customize string output
    # def __str__(self):
    #     return '\n'.join(self.entries)

j = Journal()
j.add_entry('I cried today.')
j.add_entry('I ate a bug.')

print(f'Journal entries:\n{j}')  # f-string calls __str__ internally
print(j)                          # Calls __str__ or __repr__ internally
```

### Key Points

1. **Default Object Representation**
    - Without `__str__`, printing an object shows:
        
        ```
        <module_name.ClassName object at memory_address>
        ```
        
    - Example: `<__main__.Journal at 0x168af483910>`
        - `__main__` → the module where the class is defined
        - `Journal` → class name
        - `0x168af483910` → memory address
2. **`__str__` Method**
    - Customize what `print(obj)` or `str(obj)` outputs.
    - Example:
        
        ```python
        def __str__(self):
            return '\n'.join(self.entries)
        ```
        
    - With `__str__` defined, printing `j` will display journal entries instead of default memory info.
3. **`__repr__` vs `__str__`**
    - `__str__` → user-friendly string representation (used by `print`)
    - `__repr__` → developer-friendly representation (used in interactive shell or when no `__str__`)
    

✅ **Takeaway:** Always define `__str__` in classes if you want readable `print()` output for your objects.

## **Snap Step 5 [Python Classes: Instance vs Static Methods]**

### 1️⃣ Instance-based Classes (`__init__` and `self`)

```python
class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0
```

- `__init__` → constructor, called when creating a new object.
- `self.entries` and `self.count` → **instance attributes**, each object has its own copy.
- Example:

```python
j1 = Journal()
j2 = Journal()
j1.entries.append("Hello")
print(j2.entries)  # [] → separate from j1
```

✅ **Use when each object needs its own state.**

### 2️⃣ Static Method Classes (`@staticmethod`)

```python
class PersistenceManager:
    @staticmethod
    def save_to_file(data):
        ...
```

- `@staticmethod` → does **not use `self`**, belongs to the class.
- Can be called **without creating an instance**:

```python
PersistenceManager.save_to_file(my_data)
```

- Ideal for **utility functions** that do not rely on per-object state.

### 3️⃣ Quick Comparison

| Class Type | `__init__` Needed? | When to Use |
| --- | --- | --- |
| Stateful (per-object data) | ✅ Yes | Each object maintains its own state |
| Stateless / Utility | ❌ No | Methods operate only on parameters |

✅ **Key Takeaway:**

- Use `__init__` and `self` when the class needs **per-instance state**.
- Use `@staticmethod` for **stateless utility methods** that don’t depend on object data.

## **Snap Step 6 [God Object (Anti-pattern)]**

- A **God Object** is a class that **does too much**.
- It **knows too much and controls too many things** in a program.
- Makes code **hard to maintain, test, or extend**.

**Example:**

```python
class GodObject:
    def process_users(self): ...
    def save_files(self): ...
    def send_network_request(self): ...
```

- Problem: One class handles **users, files, networking** → chaos!
- Solution: **Split responsibilities** into smaller, focused classes.

✅ **Key Idea:** “One class = one job”