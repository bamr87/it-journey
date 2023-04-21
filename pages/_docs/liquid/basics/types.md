Types
=====

Liquid objects can be one of six types:

-   [String](https://shopify.github.io/liquid/basics/types/#string)-   [Number](https://shopify.github.io/liquid/basics/types/#number)-   [Boolean](https://shopify.github.io/liquid/basics/types/#boolean)-   [Nil](https://shopify.github.io/liquid/basics/types/#nil)-   [Array](https://shopify.github.io/liquid/basics/types/#array)-   [EmptyDrop](https://shopify.github.io/liquid/basics/types/#emptydrop)

You can initialize Liquid variables using [`assign`](https://shopify.github.io/liquid/tags/variable/#assign) or [`capture`](https://shopify.github.io/liquid/tags/variable/#capture) tags.

String
------

Strings are sequences of characters wrapped in single or double quotes:

```
{% assign my_string = "Hello World!" %}

```

Liquid does not convert escape sequences into special characters.

Number
------

Numbers include floats and integers:

```
{% assign my_int = 25 %}
{% assign my_float = -39.756 %}

```

Boolean
-------

Booleans are either `true` or `false`. No quotations are necessary when declaring a boolean:

```
{% assign foo = true %}
{% assign bar = false %}

```

Nil
---

Nil is a special empty value that is returned when Liquid code has no results. It is **not** a string with the characters "nil".

Nil is [treated as false](https://shopify.github.io/liquid/basics/truthy-and-falsy/#falsy) in the conditions of `if` blocks and other Liquid tags that check the truthfulness of a statement.

In the following example, if the user does not exist (that is, `user` returns `nil`), Liquid will not print the greeting:

```
{% if user %}
  Hello {{ user.name }}!
{% endif %}

```

Tags or outputs that return `nil` will not print anything to the page.

Input

```
The current user is {{ user.name }}

```

Output

```
The current user is

```

Array
-----

Arrays hold lists of variables of any type.

### Accessing items in arrays

To access all the items in an array, you can loop through each item in the array using an [iteration tag](https://shopify.github.io/liquid/tags/iteration/).

Input

```
<!-- if site.users = "Tobi", "Laura", "Tetsuro", "Adam" -->
{% for user in site.users %}
  {{ user }}
{% endfor %}

```

Output

```
  Tobi Laura Tetsuro Adam

```

### Accessing specific items in arrays

You can use square bracket `[` `]` notation to access a specific item in an array. Array indexing starts at zero. A negative index will count from the end of the array.

Input

```
<!-- if site.users = "Tobi", "Laura", "Tetsuro", "Adam" -->
{{ site.users[0] }}
{{ site.users[1] }}
{{ site.users[-1] }}

```

Output

```
Tobi
Laura
Adam

```

### Initializing arrays

You cannot initialize arrays using only Liquid.

You can, however, use the [`split`](https://shopify.github.io/liquid/filters/split/) filter to break a string into an array of substrings.

EmptyDrop
---------

An EmptyDrop object is returned if you try to access a deleted object. In the example below, `page_1`, `page_2` and `page_3` are all EmptyDrop objects:

```
{% assign variable = "hello" %}
{% assign page_1 = pages[variable] %}
{% assign page_2 = pages["does-not-exist"] %}
{% assign page_3 = pages.this-handle-does-not-exist %}

```

### Checking for emptiness

You can check to see if an object exists or not before you access any of its attributes.

```
{% unless pages == empty %}
  <h1>{{ pages.frontpage.title }}</h1>
  <div>{{ pages.frontpage.content }}</div>
{% endunless %}

```

Both empty strings and empty arrays will return `true` if checked for equivalence with `empty`.