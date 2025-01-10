# Contributing to Standard Exchange Python API Client

![contributooooor](memes/image.png)

Thank you for considering contributing to the Standard Exchange Python API Client! We welcome contributions from the community to help improve and enhance the project.

## Standard Python client

This is a Python client for connecting to the Standard Exchange. It provides a set of asynchronous methods to interact with the exchange's API and contract functions, allowing you to fetch order books, trade histories, token information, submit limit/market orders, and more.

## How to Contribute

### Reporting Issues

If you encounter any bugs or have suggestions for improvements, please open an issue on GitHub. Provide as much detail as possible, including steps to reproduce the issue and any relevant information about your environment.

### Forking the Repository

1. Fork the repository by clicking the "Fork" button on the GitHub page.
2. Clone your forked repository to your local machine:

    ```bash
    git clone https://github.com/your-username/standardweb3.git
    cd standardweb3
    ```

### Creating a Branch

Create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
```

### Making Changes

Make your changes to the codebase. Ensure that your code follows the project's coding standards and includes appropriate tests. For coding standards, pre-commit setting in `.pre-commit-config.yaml` will verify it for you. Standard Exchange Python Client uses [uv](https://docs.astral.sh/uv/#highlights) to run. Contributors must install this to run the project and make changes.

### Running Tests

Before submitting your changes, run the tests to ensure everything is working correctly:

```bash
# Install dependencies
uv pip install -r pyproject.toml

# Run tests
uv run pytest
```

### Committing Changes

Commit your changes with a clear and descriptive commit message:

```bash
git add -A
git commit -m "Add feature: your feature description"
```

### Pushing Changes

Push your changes to your forked repository:

```bash
git push origin feature/your-feature-name
```

### Submitting a Pull Request

1. Go to the original repository on GitHub and click the "New pull request" button.
2. Select your branch from the "compare" dropdown.
3. Provide a clear and descriptive title and description for your pull request.
4. Submit the pull request.

## Directory Structure

Here is an overview of the directory structure of the project in `src` directory:

```
standardweb3/
├── abis/                   # ABI files for smart contracts
├── api/                    # API interaction functions
├── consts/                 # Constants used in the project
├── contract/               # Contract interaction functions
├── examples/               # Example scripts
├── types/                  # Type definitions
├── __init__.py             # Initialization file
├── README.md               # Project README
├── CONTRIBUTING.md         # Contribution guidelines
└── pyproject.toml          # Project dependencies
```

## Call for Help (CFH)

We are actively seeking contributors to help with the following areas:

- Improving [documentation](https://learn.standardweb3.com)
- Writing unit tests
- Adding new features
- Fixing bugs
- Adding new examples in `examples/` folder

If you are interested in contributing, please check the open issues on GitHub or contact us directly at [contact at standardweb3.com](mailto:contact@standardweb3.com)

## Contact Information

If you have any questions or need further assistance, please feel free to reach out:

- Email: contact@standardweb3.com

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for your contributions!