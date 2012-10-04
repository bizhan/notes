# JavaScript Testing: The Holy Grail
## by Adam Hawkins

### The Holy Grail

Browser independent
Written in JS
Unit and integration
Test against single browser while developing
Test against all browsers in CI
Runs from the CLI

### PhantomJS

Headless browser

Excecute JS programmatically in a real content

Real DOM

#### CasperJS

Syntactic sugar on top of PhantomJS

Integration tests

DOM interaction API

Shouldn't be used to write unit tests

Good for a small # of test cases

Tests bound PhantomJS

### JSTestDriver

Runs from the command line

Supports multiple browsers

Unclear how to do integration tests

Browser independent, but test runner depnedent

Must maintain browser installations

Tests bound to test runner

### ZombieJS

Clear support for integration tests

Build on Node

Test bounds to ZombieJS

Similar to CasperJS + PhantomJS

### Capybara

Tests written in Ruby

Multiple adapters for headless or real browsers

Easy to maintain large test suites

Test code and app code exist in separate threads (may be confusing)

### Problems

No unified framework for unit and integration

Dependency hell

Tests bound to test runner

Not all methods CLI friendly

### Approaching the Holy Grail

- Remove test runner dependence
- Unify integration and unit
- Run in headless browser for local tests
- Run in real browser in CI
- Try to do it with JS

TestSwarm for CI with multiple browsers

Check out [Iridium](http://github.com/radiumsoftware/iridium)
