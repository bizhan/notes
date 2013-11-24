# S.O.L.I.D Python

## Usual OO Systems

- Rigid
- Fragile
- Immobile
- Viscous

## Why SOLID?

- Maintainability, reusability, easy testing

Teniendo en cuenta que usaremos Pyhton, en orden de importancia:

- SRP: Single Responsibility Principle
- DIP: Dependency Inversion Principle
- OCP: Open/closed principle
- LSP: Liskov Substitution Principle
- ISP: Interface segregation Principle

Principles, not rules

## SRP

- Debería haber un único motivo para cambiar la clase
  * Persistencia, Notificación, etc.
- Evitar sobrecargar clases con responsabilidades distintas
- Composición
- Da lugar a muchos objetos y muy pequeños

## DIP

- Depend upon abstractions, not upon concretion
- Compilation/Startup time dependency
```python
from package import module
```
- Runtime dependency
```python
self.collaborator.message()
```
- Concrete APIs are a smell: `SMSNotifier.send_sms('foo')` VS. `Notifier.send('foo')`
- If we don't apply DIP we end up with implicit dependencies, which are rigid
  and difficult to test

MAIN (puts together the application)
- Factory
- Configuration
APPLICATION (doesn't know about MAIN)
- Concrete implementations
- Domain

## OCP

- Facilidad de extensión sin modificar el original

## LSP

- La clase que deriva y la base son intercambiables
- En una línea de herencia no debería tener que tratar a una clase de forma
  distinta a las demás
- Los tipos derivados deben ser sustituibles por sus tipos base

## ISP

- No aplica tanto a Python
- Una interfaz pequeña es una interfaz mejor
