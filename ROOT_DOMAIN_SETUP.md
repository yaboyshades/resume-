# Root Domain Setup

To make your resume accessible at `https://yaboyshades.github.io` (without `/resume-`):

1. Create a new repository named `yaboyshades.github.io`
2. Add an `index.html` file with this content:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=https://yaboyshades.github.io/resume-/">
    <title>Anthony Leaman - Resume</title>
</head>
<body>
    <p>Redirecting to <a href="https://yaboyshades.github.io/resume-/">my resume</a>...</p>
</body>
</html>
```

3. Commit and push to deploy

This will make both URLs work:
- `https://yaboyshades.github.io` → redirects to resume
- `https://yaboyshades.github.io/resume-` → main resume site