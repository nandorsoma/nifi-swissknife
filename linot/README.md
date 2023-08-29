# LICENSE/NOTICE generator

This cli tool helps you to generate the license files. When you find a bundle that is missing license
info, please update this tool based on the [When a licensing info not found](#When a licensing info not found)
section.

### Usage

Requires python3

`python3 linot.py <path_to_nar> <path_to_output>`

`path_to_nar` is the nar for which we are about to generate the NOTICE and LICENSE files.

In the generated `NOTICE` file replace `<module-name>` with the name of the nar.

### When a licensing info not found

In that case the output should be something like that:
```
Licensing info found for these bundles:
  - commons-codec, found: NOTICE
  - bval-jsr, found: NOTICE
  - jackson-dataformat-csv, found: NOTICE
...
  - antlr4-runtime, found: NOTICE and LICENSE.
  - antlr-runtime, found: NOTICE
  - checker, found: NOTICE
Licensing info not found for these bundles:
  - avro-1.11.1.jar
```

In that case we need to create a file called `avro` in the `dependency-maps/<license_type>` folder.
`license_type` is the short version of the licenses that we use. For example `ASLv2` or `CDDL 1.1`.
A matching `license_type` should be also present in the `static/notice-headers` folder.

The `dependency` file should look like this:
```
<dependency-name>-<version>.jar
---NOTICE----------------------------------------------------------
  <notice information>
---LICENSE---------------------------------------------------------
  <license information>
```
License part is optional.