# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Calendar Versioning](https://calver.org/) with a `YYYY.MINOR.MICRO` format.

## Unreleased

- Table of content
- Examples

## 22.3.0-dev (2022-03-30)

### Fixed

- error converting requests without content. Now this field is optional.
- error converting responses without content. Now this field is optional.
- error creating Markdown tables containing newlines characters

## 21.1.0-dev (2021-12-19)

### Added

- add the response body section
- add the request body section
- handle nested parameters

### Changed

- the program now requires the `.yaml` file parameter
- change the parsing logic from a dictionary data type to dedicated objects


## 21.0.0-dev (2021-12-08)
First alpha release - still under heavy development