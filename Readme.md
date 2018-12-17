# Computation of points on elliptic curve

Program reads field parameters, elliptic curve
coefficients and a set of computation instructions
form input file and writes calculation result of
each instruction in output file.

### Run program:

```sh
python3 main.py
```

Or

```sh
make run
```

### Optional parameters

1. `-i`, `--input` - input file path
2. `-o`, `--output` - output file path
3. `-d`, `--debug` - debug information logging mode
4. `-h`, `--help` - show help message

### Input file format

<table>
    <thead>
        <th>Line number</th>
        <th>Description</th>
        <th>p</th>
        <th>s</th>
        <th>n</th>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Field type</td>
            <td>Z<sub>p</sub></td>
            <td>A field of characteristic 2, supersingular curve</td>
            <td>A field of characteristic 2, nonsupersingular curve</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Field</td>
            <td>Prime number</td>
            <td colspan="2">An irreducible polynomial over a field Z<sub>2</sub> introducted by a nonzero powers list</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Curve</td>
            <td>a b</td>
            <td colspan="2">a b c</td>
        </tr>
        <tr>
            <td>>= 4</td>
            <td>Instructions</td>
            <td colspan="3"><code>(1, 2) + (3, 4)</code> or <code>(1, 2) * 5</code></td>
        </tr>
    </tbody>
</table>

Next radices are supported:
1. Binary: `0b0101101`
2. Octal: `0o54`
3. Decimal: `10`
4. Hexadecimal: `0xd00`

### Output file format

```
(1, 2) + (3, 4) = (5, 6)
(1, 2) * 5 = (7, 8)
```

### Examples

<table>
    <thead>
        <th>input.txt</th>
        <th>output.txt</th>
    </thead>
    <tbody>
        <tr>
            <td>
                <pre>
p
5
1 1
(0, 1) + (0, 1)
(4, 2) + (0, 1)
(0, 1) * 1
(0, 1) * 2
                </pre>
            </td>
            <td>
                <pre>
(0, 1) + (0, 1) = (4, 2)
(4, 2) + (0, 1) = (2, 1)
(0, 1) * 1 = (0, 1)
(0, 1) * 2 = (4, 2)
                </pre>
            </td>
        </tr>
        <tr>
            <td>
                <pre>
n
4 1 0
1000 1001
(0b0010, 0b1111) + (0b1100, 0b1100)
(0b0011, 0b1111) + (0b1010, 0b1010)
(0b0010, 0b1111) * 1
(0b0010, 0b1111) * 2
(0b0010, 0b1111) * 12
(0b0010, 0b1111) * 22
                </pre>
            </td>
            <td>
                <pre>
(0b0010, 0b1111) + (0b1100, 0b1100) = (1111101000, 1111)
(0b0011, 0b1111) + (0b1010, 0b1010) = (1111100001, 1010)
(0b0010, 0b1111) * 1 = (0010, 1111)
(0b0010, 0b1111) * 2 = (1111101001, 1110)
(0b0010, 0b1111) * 12 = (1111100001, 1000)
(0b0010, 0b1111) * 22 = (1111100111, 0111)
                </pre>
            </td>
        </tr>
    </tbody>
</table>

### Makefile

Script | Description
------ | -----------
`dev` | Developing mode
`deps` | Dependencies setup
`run` | Run program
`lint` | Run linting tools
`test` | Run tests
