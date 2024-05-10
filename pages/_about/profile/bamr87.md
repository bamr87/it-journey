---
name: Amr Abdel-Motaleb
avatar: /path/to/avatar.png
bio: A brief description about yourself
location: Your location
email: your.email@example.com
website: https://yourwebsite.com
github: your-github-username
twitter: your-twitter-handle
linkedin: your-linkedin-username
lastmod: 2024-05-10T04:18:29.592Z
permalink: /about/bamr87/
---


# Navigate to your current repository

`cd ~/github/it-journey`

# Add the GitHub profile repository as a remote repository

`git remote add bamr87 https://github.com/bamr87/bamr87.git`

# Add the remote repository as a subtree

`git subtree add --prefix=pages/_about/contributors/bamr87 bamr87 main`

<!-- Include the library. -->
<script
  src="https://unpkg.com/github-calendar@latest/dist/github-calendar.min.js">
</script>

<!-- Optionally, include the theme (if you don't want to struggle to write the CSS) -->
<link
  rel="stylesheet"
  href="https://unpkg.com/github-calendar@latest/dist/github-calendar-responsive.css"
/>

<!-- Prepare a container for your calendar. -->
<div class="calendar">
    <!-- Loading stuff -->
    Loading the data just for you.
</div>

<script>

// or enable responsive functionality:
    GitHubCalendar(".calendar", "bamr87", { responsive: true });

</script>

