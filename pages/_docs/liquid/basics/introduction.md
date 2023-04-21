Introduction
============

Liquid uses a combination of [**objects**](https://shopify.github.io/liquid/basics/introduction/#objects), [**tags**](https://shopify.github.io/liquid/basics/introduction/#tags), and [**filters**](https://shopify.github.io/liquid/basics/introduction/#filters) inside **template files** to display dynamic content.

Objects
-------

**Objects** contain the content that Liquid displays on a page. Objects and variables are displayed when enclosed in double curly braces: `{{` and `}}`.

Input

```
{{ page.title }}

```

Output

```
Introduction

```

In this case, Liquid is rendering the content of the `title` property of the `page` object, which contains the text `Introduction`.

Tags
----

**Tags** create the logic and control flow for templates. The curly brace percentage delimiters `{%` and `%}` and the text that they surround do not produce any visible output when the template is rendered. This lets you assign variables and create conditions or loops without showing any of the Liquid logic on the page.

Input

```
{% if user %}
  Hello {{ user.name }}!
{% endif %}

```

Output

```
  Hello Adam!

```

Tags can be categorized into various types:

-   [Control flow](https://shopify.github.io/liquid/tags/control-flow/)-   [Iteration](https://shopify.github.io/liquid/tags/iteration/)-   [Template](https://shopify.github.io/liquid/tags/template/)-   [Variable assignment](https://shopify.github.io/liquid/tags/variable/)

You can read more about each type of tag in their respective sections.

Filters
-------

**Filters** change the output of a Liquid object or variable. They are used within double curly braces `{{ }}` and [variable assignment](https://shopify.github.io/liquid/tags/variable/), and are separated by a pipe character `|`.

Input

```
{{ "/my/fancy/url" | append: ".html" }}

```

Output

```
/my/fancy/url.html

```

Multiple filters can be used on one output, and are applied from left to right.

Input

```
{{ "adam!" | capitalize | prepend: "Hello " }}

```

Output

```
Hello Adam!
```