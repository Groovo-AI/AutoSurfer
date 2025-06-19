# 🤝 Contributing to AutoSurfer

Thank you for your interest in contributing to **AutoSurfer** — an open-source platform where browser-native AI agents live digital lives.

We welcome contributors of all skill levels. Whether you're improving docs, fixing bugs, building new features, or creating new agent personas — you're helping shape the future of lifelike AI automation.

---

## 🧠 What Is AutoSurfer?

AutoSurfer is a framework for launching autonomous browser agents with memory, personality, and mood. These agents interact with the internet like humans — clicking, scrolling, thinking, and evolving.

---

## 🛠️ How to Get Started

### 1. **Fork the Repo**

Click the **Fork** button on GitHub and clone your fork locally

### 2. **Install Requirements**

Make sure you have Python 3.11+ and [`uv`](https://github.com/astral-sh/uv):

```bash
uv sync
playwright install
```

### 3. **Run the Dev Agent**

```bash
make dev
```

This will open a browser window with UI annotation enabled.

---

## 🧩 What You Can Contribute

| Area                | Examples                                              |
| ------------------- | ----------------------------------------------------- |
| **Features**        | Task planner, mood engine, persona generator          |
| **LLM Prompting**   | Better system prompts, memory formats                 |
| **DOM Logic**       | Improved UI element filtering/highlighting            |
| **Agent Templates** | Add a "researcher", "engager", "form filler"          |
| **Docs & Guides**   | Setup help, use case tutorials, architecture overview |
| **Bug Fixes**       | Edge cases, stability improvements                    |
| **Testing**         | Unit tests for memory, annotation, selectors          |

---

## 🧾 Coding Conventions

- Use `snake_case` for Python variables and functions.
- Add type hints and docstrings.
- Keep functions short and composable.
- Use `logger` for debug/info messages.
- For JavaScript, keep everything modular and scoped in IIFEs or functions.

---

## 🐛 Submitting Issues

Found a bug or want to propose a new feature?

1. Search the [existing issues](https://github.com/Groovo-AI/AutoSurfer/issues)
2. If not found, [open a new issue](https://github.com/Groovo-AI/AutoSurfer/issues/new)
3. Use labels like `bug`, `enhancement`, `question`, `good first issue`

---

## 🔁 Pull Request Workflow

1. **Create a new branch**

   ```bash
   git checkout -b your-feature-name
   ```

2. **Make your changes**

3. **Run and test your code**

4. **Commit**

   ```bash
   git commit -m "feat: add agent memory handler"
   ```

5. **Push and open a pull request**

   ```bash
   git push origin your-feature-name
   ```

We'll review your PR and work with you to get it merged! 🚀

---

## 🌟 Code of Conduct

Be respectful, inclusive, and constructive. We're building something amazing together.

---

## 💬 Need Help?

We’re launching a community soon. For now, feel free to:

- Open a GitHub Issue
- DM the creator [@developeranku](https://github.com/developeranku)

---

Thank you for contributing to AutoSurfer. Let’s build the future of AI agents — together.
