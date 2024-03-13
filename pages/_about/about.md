---
title: About
layout: collection
collection: post
permalink: /about/
lastmod: 2022-06-17T02:01:09.704Z
---

# About this site

For those of you who have stumbled upon this partially completed website, as you can see, there's not much useful information here. I'm attempting to build this site while covering fundamental concepts and tools used to build "Information Systems". Obviously, if you're familiar with the subject, it's a huge undertaking, and there's no right way to approach it and there are many technologies to choose from.

Within this site, I attempt to utilize open source technologies and free services so anyone, and everyone, can learn. Not only will you learn how these technologies work that make up the "Internet", but you might find some of these tools/techniques useful in your everyday life, such as journalizing your day, or capturing recipes for later use. This site should be understood by anyone who wants to embark on this journey to learn "IT", and will hopefully give you everything you need to become a full stack developers, if you so choose to.

I chose the domain `{{ site.logo_source }}` because I hope this site will provide a lifelong learning experience for anyone who wants to learn how to code and build information systems that help them with everyday life.

[Life Hack Wiki](https://en.wikipedia.org/wiki/Life_hack) 

## Quick Facts

This world was created by {{ site.founder }} and maintained by:

Name | Profile
---------|----------
{% for follower in site.maintainers -%}
  {{ follower.name }} | {{ follower.profile }}
{% endfor %}


And, most importantly, Powered By:

Name | Link
---------|----------
{% for power in site.powered_by -%}
{{ power.name }} | {{ power.url }}
{% endfor %}

## Principles

When developing an open source project, embracing certain key principles can significantly enhance its success, impact, and sustainability. These principles include the "DRY" (Don't Repeat Yourself) principle, which emphasizes code efficiency and maintainability by avoiding repetition; the "Design for Failure" principle, which prepares the project to gracefully handle and recover from errors; the "KIS" (Keep It Simple) principle, advocating for simplicity in design to improve user experience and ease of maintenance; the "REnO" (Release Early and Often) principle, which encourages frequent updates to incorporate user feedback and iterate quickly; and the "MVP" (Minimum Viable Product) approach, focusing on launching with essential features to test hypotheses and refine based on real-world use.

Additionally, the collaborative essence of open source development is fundamental, leveraging the diverse expertise, creativity, and innovation of a global community. This collaboration accelerates problem-solving, enhances the quality and reliability of the software, facilitates rapid innovation, and fosters a supportive community of developers. It ensures the project's growth, sustainability, and relevance by adapting to user needs and technological advances. In summary, these principles and the collaborative spirit are the cornerstones of successful open source projects, driving their development, impact, and longevity in the ever-evolving landscape of technology.

[Programming principles Wiki](https://en.wikipedia.org/wiki/Category:Programming_principles)

### Design for failure - DFF

"Design for Failure" is a principle that sounds a bit like planning a grand banquet in a castle while also preparing for an unexpected dragon attack. In the realm of programming and information systems, it's the art of building systems that are resilient and can gracefully handle the inevitable hiccups, outages, or disasters that may occur.

Imagine you're constructing a magical tower that needs to stay upright even if one of its supporting spells fails. In this scenario, "Design for Failure" means you've cleverly crafted backup spells and redundancies so that if one spell fizzles out, the tower doesn't crumble into fairy dust. It's an acknowledgment that in the real world (or any sufficiently complex magical world), things will go wrong. The goal is to ensure these mishaps don't result in catastrophic failures.

Here's how it breaks down:

1. **Expectation of Failure**: Just as a wise wizard expects their experiments to sometimes go awry, systems are designed with the understanding that components can and will fail. This mindset shifts from "if" to "when" failure will happen, leading to more robust designs.

2. **Redundancy and Failovers**: Like having multiple magical conduits for your energy source, systems are built with backup components that can take over if the primary one fails. This might mean having duplicate databases, servers, or even entire data centers ready to pick up the slack without users noticing a thing.

3. **Graceful Degradation**: Imagine a spell that can scale its power down smoothly under pressure, rather than just fizzling out. In tech terms, systems should still operate in a reduced mode instead of completely failing. This might mean some non-critical features are temporarily unavailable, but the core functionality remains intact.

4. **Monitoring and Alerts**: Just as a network of crystal balls could alert you to disturbances across the kingdom, effective systems have comprehensive monitoring to detect and alert on issues in real-time. This allows for swift identification and resolution of problems, often before users are even aware there was an issue.

5. **Disaster Recovery Plans**: Having a plan to quickly restore operations after a catastrophe is like knowing a powerful restoration spell after a dragon attack. This involves backups, data recovery processes, and clear procedures for getting back to normal operations as swiftly as possible.

6. **Testing for Failure**: Finally, actively testing systems for failure—through methods like chaos engineering (intentionally introducing problems to test resilience)—is akin to stress-testing your magical defenses in a controlled environment. It helps identify weaknesses before they become real problems.

Designing for failure means accepting the reality of potential problems and preparing for them, rather than merely reacting when they occur. It's about building systems that are not just resilient in theory but proven to be so through careful planning, redundancy, monitoring, and continuous testing. In the grand tapestry of programming and information systems, it's a principle that weaves resilience into the very fabric of technology, ensuring that services can endure and thrive, even when faced with the unexpected.

### Don't repeat yourself - DRY

The "DRY" principle—a classic mantra in the world of programming, standing for "Don't Repeat Yourself." This principle suggests that you should avoid duplicating code across your projects. Instead of having the same code in multiple places, the idea is to have a single, definitive source. This way, if you need to make a change, you only have to do it in one spot, reducing the chance of errors and inconsistencies. It's like having a single recipe for a magical potion; if you decide to tweak the formula, you only have to update it in one ancient, mystical book rather than in a dozen scrolls scattered across the kingdom.

Now, let's juxtapose this with the notion of repeating yourself for practice. On the surface, it might seem contradictory to the DRY principle. However, in the context of learning and mastering programming (or any skill, really), repetition is your ally. It's like practicing spells or sword fighting; the more you practice, the stronger and more instinctive your skills become.

Here's how these two ideas coexist harmoniously:

1. **In Code**: The DRY principle is about efficiency and maintainability in your codebase. It's a strategy to avoid redundancy, making sure that every piece of knowledge has a single, unambiguous representation in the system. It's about not having the same logic spread across multiple parts of your application, which can lead to errors when changes are made.

2. **In Learning**: When learning to code, repeating tasks, writing code, and solving problems multiple times helps solidify your understanding and improve your skills. Each repetition helps deepen your comprehension, refine your techniques, and increase your speed. It's about embedding knowledge and skill through practice, much like a wizard mastering a complex spell through repetition.

In essence, while the DRY principle advises against redundancy in your code to improve maintainability and efficiency, repeating coding exercises for practice is beneficial for learning, much like rehearsing lines for a play or practicing chords on a lute. This kind of repetition engrains concepts, patterns, and best practices in your mind, making you a more competent and confident coder.

So, remember: Keep your code DRY, but keep your practice wet with repetition! Let each loop through the cycle of practice water the seeds of your growing skills, and watch as your garden of knowledge blooms.

### Keep it simple - KIS

The "KIS" principle, or "Keep It Simple," is a guiding light in the realms of programming, design, and beyond, much like the principle of using a single, powerful spell instead of a convoluted combination of minor enchantments. It's a call to embrace simplicity and avoid unnecessary complexity, ensuring that systems, applications, and processes are as straightforward and efficient as possible.

Imagine you're a wizard concocting a potion. The KIS principle would advise against using 20 ingredients when 5 will achieve the same effect. It's about focusing on what's essential, making your potion not only easier to brew but also more reliable and easier to replicate or modify by other wizards in the future.

In the context of programming and information systems, here's what the KIS principle entails:

1. **Clarity Over Cleverness**: It's tempting to use intricate, clever solutions to solve problems. However, simplicity prioritizes clear and understandable code over showcasing one's prowess with complex algorithms that might confuse others (or even yourself when you revisit the code moons later).

2. **Maintainability**: Simple systems are easier to maintain. When your magical incantations (or code) are straightforward, identifying and rectifying issues becomes much less of a headache. It's like having a spellbook written in plain language rather than in cryptic runes.

3. **Efficiency**: Simple solutions often run faster and use fewer resources. It's akin to using a single, well-aimed arrow to take down a target rather than a barrage of spells. By focusing on efficiency, you ensure that your systems are not bogged down by unnecessary complexities.

4. **Ease of Collaboration**: When your work is simple and clear, other programmers (or fellow wizards) can easily understand and contribute to it. It's like writing your spell formulas in a common tongue rather than a forgotten dialect; it encourages collaboration and knowledge sharing.

5. **Focus on the End-User**: Ultimately, the goal of most projects is to serve users, not to showcase technical virtuosity. A simple interface or process that users can navigate intuitively is often more effective than a feature-rich but convoluted system. Think of it as creating a user-friendly spell that anyone can cast, not just the most learned mages.

6. **Reduced Error Margin**: Simpler systems have fewer moving parts, which means there's less that can go wrong. It's easier to ensure the integrity of a straightforward enchantment than a complex, multi-layered magical barrier.

Applying the KIS principle doesn't mean avoiding complexity at all costs or dumbing down sophisticated ideas. Rather, it's about finding the most direct and efficient path to achieve your goals, ensuring that every element serves a purpose. It's about elegance in simplicity, crafting solutions that are both powerful and accessible, much like a masterfully simple spell that achieves exactly what's needed, no more, no less.

### Release early and often - REnO

The "REnO" principle, standing for "Release Early and Often," is akin to the strategy of a wizard unveiling spells to the public incrementally to gather feedback, refine their magic, and adapt quickly to the needs of their community. In the realms of software development and information technology, this principle emphasizes the benefits of releasing new versions of a product frequently, rather than waiting to perfect every detail before making it available to users.

Imagine you're crafting a magical artifact intended to help the villagers with their daily chores. Instead of toiling in secrecy for years to perfect the artifact, you decide to release a basic version early. This initial offering has the core functionality but lacks some of the advanced features you've envisioned. By doing so, you allow the villagers to start benefiting from your creation right away. You also gain valuable insights from their experiences, which inform your subsequent improvements and additions to the artifact.

Here's how the REnO principle unfolds in the tech world:

1. **Feedback Loop**: Releasing early and often creates a continuous feedback loop with users. Just as a wizard learns from the villagers' use of the magical artifact, developers can quickly identify what works, what doesn't, and what users actually need or want. This feedback is invaluable for making timely adjustments.

2. **Faster Iterations**: By adopting a cycle of frequent releases, you can iteratively improve your product. This approach allows you to address issues, add features, and refine the user experience in smaller, manageable increments. It's like refining a potion recipe over time, adding a pinch of this or a dash of that, until it's just right.

3. **Reduce Risk**: When you release early and often, each release tends to be less monumental and, therefore, less risky. If a particular update doesn't hit the mark, the stakes are lower, and it's easier to course-correct. It's akin to testing a new spell in a controlled environment before attempting to cast it in a high-stakes situation.

4. **Adaptability**: This principle enhances your ability to adapt to changes in the market, technology, and user preferences. Just as a wizard must adjust their strategies based on the evolving needs of their community, developers can pivot more easily when they're not locked into a lengthy development cycle.

5. **Builds Engagement**: Early and frequent releases help maintain user interest and engagement. It's like a bard releasing songs in a serial fashion, keeping their audience excited for the next installment. Users appreciate seeing regular improvements and being part of a product's evolution.

6. **Learning and Growth**: For development teams, the REnO principle encourages a culture of learning and experimentation. It allows developers to try new things, learn from real-world use, and grow their skills incrementally. It's akin to a young mage honing their skills through constant practice and real-world application.

By embracing the "Release Early and Often" principle, developers can create a more dynamic, responsive, and user-focused development process. It's a philosophy that values progress over perfection, understanding that the journey of improvement is continuous, much like the quest for knowledge and mastery in the magical arts.

### Minimal Viable Path - MVP

The MVP, or in this context, let's call it the "Minimal Viable Path" to align with our adventurous theme, though it's more widely known as "Minimum Viable Product." Picture yourself as an intrepid adventurer setting out on a quest. Your goal is to reach a distant, legendary treasure. However, the path is unknown and fraught with perils. Instead of trying to map out the perfect route from the start, laden with every possible supply you might need, you choose a simpler, more agile approach. You select just enough provisions to get you to the first landmark on your journey. This strategy allows you to adapt and learn as you go, making it easier to overcome obstacles and ultimately reach your treasure more efficiently.

In the world of software development and product design, the MVP principle is similarly about starting with the simplest version of a new product or feature that allows you to begin the journey towards your ultimate goal. This version has just enough features to satisfy early adopters and provide valuable insights without the full complexity that the final product will have. Here’s how it breaks down:

1. **Focus on Core Value**: The MVP hones in on the essential functionality that solves a core problem for users. Imagine a spell that needs to transport someone a short distance. The MVP version of this spell would focus purely on the transportation aspect, without additional features like speed variations or comfort enhancements.

2. **Feedback and Iteration**: By releasing this streamlined version to users, you can gather feedback early in the process. This is akin to checking your compass and surroundings as you reach that first landmark, ensuring you’re on the right path. User feedback helps you understand if your direction is correct and what improvements or adjustments are needed.

3. **Efficient Use of Resources**: The MVP approach conserves resources, such as time and magical energy (or in the real world, money and developer effort). It allows you to test hypotheses about your product without committing to building the entire thing upfront. It’s like packing light for the initial phase of your quest, saving the bulk of your provisions for when you’re sure of your path.

4. **Quicker Time to Market**: By focusing on the minimal set of features, you can launch your product or feature much quicker. This rapid launch lets you enter the market before fully committing to a specific solution, similar to setting up a base camp quickly to claim a strategic spot on your map.

5. **Adaptability**: An MVP is designed with flexibility in mind, allowing you to pivot or adjust your approach based on real-world learning. This adaptability is crucial in a landscape that might shift or reveal new paths as you progress. It’s like finding a hidden trail that makes your quest easier, which you wouldn’t have seen without venturing out initially.

6. **Risk Reduction**: Launching an MVP helps mitigate the risk of building something that users don’t want or need. By investing in only the essential features at first, you reduce the potential loss if the product doesn’t resonate with your audience. It’s the difference between risking a small skirmish versus a full-on battle without knowing your enemy’s strength.

In essence, the MVP or "Minimal Viable Path" principle is about embarking on your grand quest with just enough to get started, learning as you go, and adapting your strategy based on real-world feedback. This approach ensures you’re not blindly following a map to treasure that might not exist but instead navigating the landscape as it unfolds, making informed decisions at each step of your journey.

### Collaborate - COLAB

Collaboration in open source development is akin to a grand council of wizards coming together to craft a powerful, communal spell. Each wizard brings their own expertise, insights, and magic to the table, enriching the spell far beyond what any one of them could achieve alone. This collective endeavor not only creates a more potent magic but also fosters a sense of community and shared purpose. Similarly, collaboration in open source development harnesses the collective intelligence, skills, and creativity of a global community to create software that is robust, innovative, and widely accessible.

Here's why collaboration is so crucial in open source development:

1. **Diverse Expertise**: Just as a council of wizards might include experts in defensive spells, potion-making, and elemental magic, open source projects benefit from the contributions of developers with varied skills and backgrounds. This diversity leads to more creative solutions, as different perspectives tackle problems in unique ways.

2. **Rapid Innovation**: Collaboration accelerates innovation. With many contributors working on a project, new features and improvements can be developed, tested, and deployed much faster than if a single developer or small team were working in isolation. It's like a group of mages pooling their energy to cast spells more quickly and powerfully.

3. **Quality and Reliability**: Open source projects undergo rigorous scrutiny from the community. Bugs and vulnerabilities are more likely to be identified and fixed promptly when a large, engaged community is actively using and examining the code. This peer review process is similar to a magical artifact being tested and refined by several experienced enchanters to ensure its reliability.

4. **Learning and Growth**: Contributing to open source projects offers an unparalleled learning experience. Developers can learn from more experienced peers, gain feedback on their contributions, and develop new skills. It's akin to an apprentice learning from a collective of master wizards, each offering wisdom in their area of expertise.

5. **Sustainability**: Collaboration ensures the sustainability of open source projects. When a project relies on a single developer or a small team, it's vulnerable to abandonment if those individuals lose interest or are unable to continue their work. A collaborative project, supported by a community, is more likely to continue thriving even as individual contributors come and go.

6. **Community and Support**: Open source development fosters a strong sense of community among contributors. This community provides not just technical support, but also moral and motivational support. It's the difference between a lone wizard facing the world and a powerful guild where members support and uplift each other.

7. **Global Impact**: Finally, collaboration in open source development allows for the creation of software that has a global impact. Just as the combined efforts of wizards from different lands can create magic with far-reaching benefits, open source projects can address needs and solve problems for people all over the world, transcending geographical and cultural boundaries.

In essence, collaboration in open source development embodies the principle that "together, we are stronger." It leverages the collective power of a global community to build software that is more innovative, reliable, and impactful than what could be achieved in isolation. Just like in a magical world, where the combined efforts of many can create wonders far beyond the reach of any individual, open source development thrives on collaboration, making the digital realm a richer, more inclusive, and more innovative space.
