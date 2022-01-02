---
title: Programming
description: Collection of programming languages notes
collection: notes
permalink: /notes/programming-languages/
lastmod: '2022-01-02T03:39:23.888Z'
---

## python

```python
print "hello world"
```

## java

```java
import javax.swing.JFrame;  //Importing class JFrame
import javax.swing.JLabel;  //Importing class JLabel
public class HelloWorld {
    public static void main(String[] args) {
        JFrame frame = new JFrame();           //Creating frame
        frame.setTitle("Hi!");                 //Setting title frame
        frame.add(new JLabel("Hello, world!"));//Adding text to frame
        frame.pack();                          //Setting size to smallest
        frame.setLocationRelativeTo(null);     //Centering frame
        frame.setVisible(true);                //Showing frame
    }
}
```

## javascript

```javascript
document.write('Hello, world!');
```

```c
#include 
 
int main(void)
{
    puts("Hello, world!");
}
```
```c++
#include 
 
int main()
{
    std::cout << "Hello, world!
";
    return 0;
}
```

## html

```html
<p>Hello World!</p>
```

## scss

```scss
$font-stack:    Helvetica, sans-serif;
$primary-color: #333;

body{
  font: 100% $font-stack;
  color: $primary-color;
}
```

## css

```css
body {
  font: 100% Helvetica, sans-serif;
  color: #333;
}
```

## sql

```sql
SELECT column_name(s)
FROM table1
LEFT JOIN table2
ON table1.column_name = table2.column_name;
```

## php

```php
<?php
echo "My first PHP script!";
?>
```

## LaTeX

```LaTeX
%-----------Technical SKILLS-----------
\section{Technical / Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
      \textbf{Databases}{: Microsoft SQL, Postgres, MySQL, Google Big Query, AWS DynamoDB, Progress DB, Oracle SQL, Teradata} \\
      \textbf{DevOps}{: GitHub, UML notation, Continuous Integration, Server Management, Linux Package Managers} \\
      \textbf{Languages}{: Bash, PowerShell, Python, Java, C, HTML, CSS, JavaScript, SQL, Progress 4GL, PHP, LaTeX} \\
      \textbf{Developer Tools}{: VS Code, Eclipse, Google Cloud SDK, Android Studio, Atom, UI Path} \\
      \textbf{Technologies/Frameworks}{: Linux, Jenkins, GitHub, JUnit, WordPress} \\
      \textbf{Operating Systems}{: Microsoft Server, RedHat Enterprise Linux, CentOS, Debian } \\
      \textbf{IDEs}{: Eclipse, VS Code, Android Studio, Atom} \\
      \textbf{Web and Integration Technologies}{: Q-Xtend, RESTful Web API's, HTML5, CSS3, XML, JSON, Kubernetes, Docker, Apache Tomcat} \\
      \textbf{Cloud Apps}{: Microsoft Power Automate, Google Appsheet, Amazon Web Services, Google Cloud Platform, Azure, Zapier} \\
      \textbf{Enterprise Applications}{: QAD ERP, Mfg/Pro, QAD EAM, Infor SyteLine, Infor ERP LN, Baan IV ERP, PeopleSoft Financials, HFM, Oracle Agile PLM} \\
      \textbf{Mobile Apps}{: Android, iOS, React Native, Swift, Java, Kotlin} \\
      \textbf{Cloud Services}{: AWS, Google Cloud Platform, Azure, Google Appsheet, Amazon Web Services, Google Cloud BigQuery,} \\
      \textbf{Web UI Frameworks}{: Angular, React} \\
      \textbf{CI/CD Frameworks}{: TeamCity, Jenkins} \\
      \textbf{Containers}{: Kubernetes, Docker} \\

    }}
  \end{itemize}
 \vspace{-16pt}
```

## Progress 4GL

```progress
define var i as int.
i=0.

for each vd_mstr no-lock where vd_addr begins "e":
	display vd_addr vd_curr.
	i = i + 1.
end.
display i
```
