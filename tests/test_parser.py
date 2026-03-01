import pytest
from tests.utils import Parser


# ================= BASIC PROGRAM STRUCTURE =================

def test_001():
    """Empty program"""
    assert Parser("").parse() == "success"


def test_002():
    """Only main function"""
    assert Parser("void main() {}").parse() == "success"


def test_003():
    """Simple main with statement"""
    source = """void main() {
        printString("Hello, World!");
    }"""
    assert Parser(source).parse() == "success"


# ================= FUNCTION DECLARATIONS =================

def test_004():
    """Multiple functions"""
    source = """
    int add(int x, int y) { return x + y; }
    int mul(int x, int y) { return x * y; }
    void main() {
        auto a = add(1,2);
        auto b = mul(3,4);
    }
    """
    assert Parser(source).parse() == "success"


def test_005():
    """Recursive function"""
    source = """
    int fact(int n) {
        if (n <= 1) return 1;
        return n * fact(n - 1);
    }
    void main() {
        printInt(fact(5));
    }
    """
    assert Parser(source).parse() == "success"


def test_006():
    """Nested function calls"""
    source = """
    int inc(int x) { return x + 1; }
    int dbl(int x) { return x * 2; }
    void main() {
        auto r = inc(dbl(5));
    }
    """
    assert Parser(source).parse() == "success"


# ================= STRUCTS =================

def test_007():
    """Struct declaration"""
    assert Parser("struct Point { int x; int y; };").parse() == "success"


def test_008():
    """Struct initialization and access"""
    source = """
    struct Point { int x; int y; };
    void main() {
        Point p = {1,2};
        printInt(p.x);
    }
    """
    assert Parser(source).parse() == "success"


def test_009():
    """Nested structs"""
    source = """
    struct A { int x; };
    struct B { A a; };
    struct C { B b; };
    void main() {
        C c;
        c.b.a.x = 10;
    }
    """
    assert Parser(source).parse() == "success"


# ================= CONTROL FLOW =================

def test_010():
    """If statement"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_011():
    """If-else statement"""
    source = """
    void main() {
        if (1) printInt(1);
        else printInt(0);
    }
    """
    assert Parser(source).parse() == "success"


def test_012():
    """While loop with break/continue"""
    source = """
    void main() {
        int i = 0;
        while (i < 10) {
            i = i + 1;
            if (i == 5) continue;
            if (i == 8) break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_013():
    """For loop"""
    source = """
    void main() {
        for (int i = 0; i < 10; i = i + 1)
            printInt(i);
    }
    """
    assert Parser(source).parse() == "success"


def test_014():
    """Switch statement"""
    source = """
    void main() {
        switch (x) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
            default: printInt(0);
        }
    }
    """
    assert Parser(source).parse() == "success"


# ================= EXPRESSIONS =================

def test_015():
    """Operator precedence"""
    source = """
    void main() {
        auto x = a + b * c - d / e;
        auto y = (a + b) * (c - d);
    }
    """
    assert Parser(source).parse() == "success"


def test_016():
    """Logical expressions"""
    source = """
    void main() {
        if (a > b && c <= d || e != f)
            printInt(1);
    }
    """
    assert Parser(source).parse() == "success"


def test_017():
    """Assignment chaining"""
    source = """
    void main() {
        int a; int b; int c;
        a = b = c = 10;
    }
    """
    assert Parser(source).parse() == "success"


def test_018():
    """Unary expressions"""
    source = """
    void main() {
        auto x = -a;
        auto y = !flag;
    }
    """
    assert Parser(source).parse() == "success"


# ================= ERROR CASES =================

def test_019():
    """Syntax error: missing )"""
    source = """
    void main( {
        printInt(1);
    }
    """
    result = Parser(source).parse()
    assert "Error" in result


def test_020():
    """Invalid auto parameter"""
    source = "void foo(auto x) {}"
    result = Parser(source).parse()
    assert "Error" in result

def test_021():
    """Empty program"""
    source = ""
    assert Parser(source).parse() == "success"


def test_022():
    """Single variable declaration"""
    source = "int a;"
    assert Parser(source).parse() == "success"


def test_023():
    """Multiple variable declarations"""
    source = "int a; float b; string c;"
    assert Parser(source).parse() == "success"


def test_024():
    """Variable with initialization"""
    source = "int a = 10;"
    assert Parser(source).parse() == "success"


def test_025():
    """Auto variable initialization"""
    source = "auto x = 1;"
    assert Parser(source).parse() == "success"


def test_026():
    """Invalid auto without initializer"""
    source = "auto x;"
    assert Parser(source).parse() == "success"


def test_027():
    """Simple function without params"""
    source = "void main() {}"
    assert Parser(source).parse() == "success"


def test_028():
    """Function with parameters"""
    source = "int sum(int a, int b) { return a + b; }"
    assert Parser(source).parse() == "success"


def test_029():
    """Function missing return semicolon"""
    source = "int f() { return 1 }"
    assert "Error" in Parser(source).parse()


def test_030():
    """Nested block statements"""
    source = """
    void main() {
        { int a; { int b; } }
    }
    """
    assert Parser(source).parse() == "success"


def test_031():
    """If statement without else"""
    source = """
    void main() {
        if (a > b) a = b;
    }
    """
    assert Parser(source).parse() == "success"


def test_032():
    """If-else statement"""
    source = """
    void main() {
        if (a > b) a = b;
        else a = 0;
    }
    """
    assert Parser(source).parse() == "success"


def test_033():
    """While loop"""
    source = """
    void main() {
        while (i < 10) i = i + 1;
    }
    """
    assert Parser(source).parse() == "success"


def test_034():
    """For loop full form"""
    source = """
    void main() {
        for (int i = 0; i < 10; i = i + 1)
            a = i;
    }
    """
    assert Parser(source).parse() == "success"


def test_035():
    """For loop missing semicolon"""
    source = """
    void main() {
        for (i = 0 i < 10; i = i + 1) {}
    }
    """
    assert "Error" in Parser(source).parse()


def test_036():
    """Return without expression"""
    source = """
    void main() {
        return;
    }
    """
    assert Parser(source).parse() == "success"


def test_037():
    """Return with expression"""
    source = """
    int f() {
        return 10;
    }
    """
    assert Parser(source).parse() == "success"


def test_038():
    """Continue inside loop"""
    source = """
    void main() {
        while (true) continue;
    }
    """
    assert Parser(source).parse() == "success"


def test_039():
    """Break inside loop"""
    source = """
    void main() {
        for (;;) break;
    }
    """
    assert Parser(source).parse() == "success"


def test_040():
    """Assignment chaining"""
    source = """
    void main() {
        int a; int b; int c;
        a = b = c = 10;
    }
    """
    assert Parser(source).parse() == "success"


def test_041():
    """Unary expressions"""
    source = """
    void main() {
        auto x = -a;
        auto y = !flag;
    }
    """
    assert Parser(source).parse() == "success"


def test_042():
    """Postfix increment"""
    source = """
    void main() {
        i++;
    }
    """
    assert Parser(source).parse() == "success"

def test_043():
    """Function call"""
    source = """
    void main() {
        foo(1, 2);
    }
    """
    assert Parser(source).parse() == "success"

def test_044():
    """Nested function calls"""
    source = """
    void main() {
        foo(bar(1), baz(2));
    }
    """
    assert Parser(source).parse() == "success"


def test_045():
    """Struct declaration"""
    source = """
    struct A {
        int x;
        float y;
    };
    """
    assert Parser(source).parse() == "success"


def test_046():
    """Struct initialization"""
    source = """
    void main() {
        A a = {1, 2.0};
    }
    """
    assert Parser(source).parse() == "success"


def test_047():
    """Struct access"""
    source = """
    void main() {
        a.b.c = 10;
    }
    """
    assert Parser(source).parse() == "success"


def test_048():
    """Invalid struct missing semicolon"""
    source = "struct A { int x; }"
    assert "Error" in Parser(source).parse()


def test_049():
    """Switch with cases"""
    source = """
    void main() {
        switch(x) {
            case 1: a = 1;
            case 2: a = 2;
            default: a = 0;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_050():
    """Switch missing colon"""
    source = """
    void main() {
        switch(x) {
            case 1 a = 1;
        }
    }
    """
    assert "Error" in Parser(source).parse()


def test_051():
    """Expression precedence"""
    source = """
    void main() {
        a = 1 + 2 * 3 < 10 && true;
    }
    """
    assert Parser(source).parse() == "success"

def test_052():
    """Multiple statements"""
    source = """
    void main() {
        a = 1;
        b = 2;
        c = a + b;
    }
    """
    assert Parser(source).parse() == "success"


def test_053():
    """Empty block"""
    source = "void main() {}"
    assert Parser(source).parse() == "success"


def test_054():
    """Nested if else"""
    source = """
    void main() {
        if (a)
            if (b) c = 1;
            else c = 2;
    }
    """
    assert Parser(source).parse() == "success"


def test_055():
    """Missing closing brace"""
    source = "void main() { int a;"
    assert "Error" in Parser(source).parse()


def test_056():
    """Invalid function parameter"""
    source = "void f(auto x) {}"
    assert "Error" in Parser(source).parse()


def test_057():
    """Multiple functions"""
    source = """
    int f() { return 1; }
    void g() {}
    """
    assert Parser(source).parse() == "success"


def test_058():
    """Function returning struct type"""
    source = "A f() { return a; }"
    assert Parser(source).parse() == "success"


def test_059():
    """Expression statement"""
    source = "a + b;"
    assert Parser(source).parse() == "success"


def test_060():
    """Invalid expression statement"""
    source = "+;"
    assert "Error" in Parser(source).parse()


def test_061():
    """Function call as expression"""
    source = "foo(1);"
    assert Parser(source).parse() == "success"


def test_062():
    """Deeply nested expression"""
    source = "a = (((b + c) * d) - e) / f;"
    assert Parser(source).parse() == "success"


def test_063():
    """Unary chain"""
    source = "a = ---b;"
    assert Parser(source).parse() == "success"

def test_064():
    """Empty switch"""
    source = "switch(x){}"
    assert Parser(source).parse() == "success"


def test_065():
    """Case without switch"""
    source = "case 1: a=1;"
    assert "Error" in Parser(source).parse()


def test_066():
    """Default without switch"""
    source = "default: a=1;"
    assert "Error" in Parser(source).parse()


def test_067():
    """Function with empty parameter list"""
    source = "void f(){}"
    assert Parser(source).parse() == "success"


def test_068():
    """Missing parameter comma"""
    source = "int f(int a int b){}"
    assert "Error" in Parser(source).parse()


def test_069():
    """Expression in for init"""
    source = """
    void main() {
        for (i = 0; i < 10; i++) {}
    }
    """
    assert Parser(source).parse() == "success"


def test_070():
    """Missing for parentheses"""
    source = "for i=0; i<10; i++ {}"
    assert "Error" in Parser(source).parse()


def test_071():
    """Nested loops"""
    source = """
    void main() {
        while(a) for(b=0;b<10;b++){}
    }
    """
    assert Parser(source).parse() == "success"


def test_072():
    """Complex struct usage"""
    source = """
    void main() {
        a.b.c(d.e);
    }
    """
    assert Parser(source).parse() == "success"


def test_073():
    """Invalid dot usage"""
    source = "a..b;"
    assert "Error" in Parser(source).parse()


def test_074():
    """Missing semicolon after expr"""
    source = "a = 1"
    assert "Error" in Parser(source).parse()


def test_075():
    """Multiple statements without semicolon"""
    source = "a=1 b=2;"
    assert "Error" in Parser(source).parse()


def test_076():
    """Struct as variable type"""
    source = "A x;"
    assert Parser(source).parse() == "success"


def test_077():
    """Function parameter as struct"""
    source = "void f(A x){}"
    assert Parser(source).parse() == "success"


def test_078():
    """Invalid struct param auto"""
    source = "void f(auto x){}"
    assert "Error" in Parser(source).parse()


def test_079():
    """Empty statement"""
    source = ";"
    assert "Error" in Parser(source).parse()


def test_080():
    """Multiple empty lines"""
    source = "\n\n"
    assert Parser(source).parse() == "success"


def test_089():
    """Expression with function and field"""
    source = "a.b(c).d;"
    assert Parser(source).parse() == "success"


def test_090():
    """Invalid function declaration missing name"""
    source = "int (){}"
    assert "Error" in Parser(source).parse()

def test_092():
    """Assignment in condition"""
    source = """
    void main() {
        if (a = b) {}
    }
    """
    assert Parser(source).parse() == "success"

def test_094():
    """Multiple unary operators"""
    source = "a = !!b;"
    assert Parser(source).parse() == "success"

def test_096():
    """Valid increment expression"""
    source = "a++;"
    assert Parser(source).parse() == "success"


def test_097():
    """Missing RPAREN in call"""
    source = "foo(1,2;"
    assert "Error" in Parser(source).parse()


def test_098():
    """Nested struct init"""
    source = "A x = { {1}, {2} };"
    assert Parser(source).parse() == "success"


def test_099():
    """Invalid empty struct init"""
    source = "A x = {};"
    assert "Error" in Parser(source).parse()


def test_100():
    """Full program stress test"""
    source = """
    struct A { int x; };
    int f(int a){ return a; }
    void main(){
        A a = {1};
        for(int i=0;i<10;i=i+1){
            if(i%2==0) continue;
            a.x = f(i);
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_085_expr_consecutive_operators_fail():
    source = "void main() { x = 5 ++ 2; }" # Parsed as (5++) 2 or 5 (++2)?
    # Usually syntax error if operands missing
    source = "void main() { x = 5 * / 2; }"
    parser = Parser(source)
    assert parser.parse() != "success"

# ==============================================================================
# GROUP 9: BLOCKS & SCOPE (5 Tests)
# ==============================================================================

def test_086_empty_block():
    source = "void main() { {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_087_nested_blocks():
    source = "void main() { { { int x; } } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_088_block_variable_shadowing():
    """Syntactically valid"""
    source = "void main() { int x; { int x; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_089_unmatched_brace_open_fail():
    source = "void main() { { }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_090_unmatched_brace_close_fail():
    source = "void main() { } }"
    parser = Parser(source)
    assert parser.parse() != "success"

# ==============================================================================
# GROUP 10: MISC & EDGE CASES (10 Tests)
# ==============================================================================

def test_091_minified_code():
    source = "struct A{int x;};void main(){if(1){x=1;}else{x=2;}}"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_092_trailing_comma_func_args_fail():
    source = "void f(int a,) {}"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_093_trailing_comma_struct_init_fail():
    """Usually C-like doesn't enforce strict check in parser for this,
       but let's assume strict grammar"""
    source = "void main() { Point p = {1, 2,}; }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_094_keyword_as_identifier_fail():
    source = "void if() {}"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_095_keyword_struct_as_id_fail():
    source = "int struct = 5;"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_096_function_call_missing_parens_fail():
    source = "void main() { f; }"
    source = "void main() { f(1, ); }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_097_statement_missing_semicolon_fail():
    source = "void main() { x = 5 }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_098_multiline_string_literal_fail():
    """Spec: Newline cannot appear directly in string"""
    source = "void main() { s = \"line1\nline2\"; }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_099_chained_access_call():
    """(function()).member"""
    source = "void main() { getPoint().x = 5; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_100_complex_program_integration():
    """Combination of everything"""
    source = """
    struct Point { int x; int y; };
    Point make(int x) { return {x, x}; }
    void main() {
        auto p = make(10);
        if (p.x > 0) {
            printInt(p.x);
        }
    }
    """
    parser = Parser(source)
    assert parser.parse() == "success"