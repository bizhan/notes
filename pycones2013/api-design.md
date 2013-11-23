# Pensando en APIs

Libro: Practical API Design

Separación de API y SPI (Service Provider Interface)

## API

- Intefaz de un programa/biblioteca con el mundo

## SPI
- La forma que un programa nos pide que ingresemos nuestro método de solución
  de un problema
- Subconjunto de API
- La interfaz de un programa con un plugin (métodos abstractos)

## Clueless

- Ignorancia es un beneficio
- No significa "no saber" sino abstraerse

## Consejos

- La primera regla de diseño: el sistema; el segundo: tu gusto y el tercero los
  estándares (Necesito - Me gusta - PEP 8)
- Las API declarativas suelen ser más fáciles de mantener, extender y
  generalizar
- Exponer lo estrictamente necesario
- Mientras menos se exponga, mejor
- Cooperar con otras APIs
  * Compatibilidad con stdlib
  * PEP 20, PEP 8
  * NO retornan objetos de otras APIs
  * NO redefinir comportamiento de otras APIs
- Prefiere NO exponer objetos como resultados de operaciones, mejor tipos primitivos
- Los controles de tipos deben hacerse a nivel de API (assert)
- Cuidado con retorno de valores nulos
- Si se van a definir objetos
  * Intentar que sean inmutables
  * Darle muchos derechos al constructor (inmutabilidad)

### Gestión de errores

- Errores == algo inmanejable por nuestra librería
- Tratarlos lo más temprano posible
- "Errors should never pass silently, Unless explicitly silenced"
- Piensa si una excepción builtin cubre el caso de tus excepciones propias
- Si declaras una Exception y nunca la expones, es altamente probable que algo
  este MAL

### Consejos finales

- Simetría (load, dump)
- No abusar de los patrones
- Evitar el monkeypatch
