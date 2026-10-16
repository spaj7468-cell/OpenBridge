# Contributing to OpenBridge

Thanks for helping improve OpenBridge.

## Before contributing

- Check the roadmap and current compatibility matrix.
- Keep feature status honest: planned, experimental, tested, or stable.
- Do not add secrets, API keys, personal project data, or private browser content.
- Prefer small, reviewable changes with tests and documentation.

## Design requirements

- Do not make arbitrary shell execution or generated-script execution the default path.
- Every new tool needs a schema, permission statement, error model, and tests.
- Mutating actions need preview/approval behavior where practical.
- Local endpoints must default to loopback and validate callers.
- Browser permissions must be minimal and explained.
- Update the compatibility matrix when support is actually tested.

## Pull request checklist

- [ ] Explain the user problem and intended behavior.
- [ ] Add or update tests.
- [ ] Document new tools and their side effects.
- [ ] Add failure and disconnect behavior.
- [ ] Check logs and errors for secret leakage.
- [ ] Update the roadmap only when acceptance criteria are met.

## License

A repository license has not yet been selected. Please do not assume that all contributions can be redistributed under a particular license until that decision is made.
