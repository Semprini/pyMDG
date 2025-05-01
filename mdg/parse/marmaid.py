"""
---
title: Animal example
---

classDiagram
    note "From Duck till Zebra"

    namespace Foo {
        class Animal{
            +int age
            +String gender
            +isMammal()
            +mate()
        }
        class Duck{
            +String beakColor
            +swim()
            +quack()
        }
        class Fish{
            -int sizeInFeet
            -canEat()
        }
        class Zebra{
            +bool is_wild
            +run()
        }
    }
    Animal -- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    note for Fish "can fly\ncan swim\ncan dive\ncan help in debugging"
"""