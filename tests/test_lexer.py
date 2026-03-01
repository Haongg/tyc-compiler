import pytest
from tests.utils import Tokenizer


# ================= IDENTIFIERS & KEYWORDS =================

def test_001():
    """Identifier"""
    assert Tokenizer("abc").get_tokens_as_string() == "abc,<EOF>"


def test_002():
    """Identifier with underscore and digits"""
    assert Tokenizer("a_b_c123").get_tokens_as_string() == "a_b_c123,<EOF>"


def test_003():
    """Keyword list"""
    source = "auto break case continue default else float for if int return string struct switch void while"
    expected = (
        "auto,break,case,continue,default,else,float,for,if,int,return,"
        "string,struct,switch,void,while,<EOF>"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


# ================= NUMERIC LITERALS =================

def test_004():
    """Integer literals"""
    assert Tokenizer("42 0 255").get_tokens_as_string() == "42,0,255,<EOF>"


def test_005():
    """Float literals"""
    source = "9.0 12e8 0.33E-3 128e+42"
    assert Tokenizer(source).get_tokens_as_string() == "9.0,12e8,0.33E-3,128e+42,<EOF>"


def test_006():
    """Leading zero integer"""
    assert Tokenizer("09").get_tokens_as_string() == "09,<EOF>"


def test_007():
    """Float starting with dot"""
    assert Tokenizer(".0e-1").get_tokens_as_string() == ".0e-1,<EOF>"


# ================= STRING LITERALS =================

def test_008():
    """Simple string"""
    assert Tokenizer('"hello"').get_tokens_as_string() == "hello,<EOF>"


def test_009():
    """String with escape characters"""
    source = '"abc\\nxyz"'
    assert Tokenizer(source).get_tokens_as_string() == "abc\\nxyz,<EOF>"


def test_010():
    """String with escaped quote"""
    source = '"abc\\\"def"'
    assert Tokenizer(source).get_tokens_as_string() == "abc\\\"def,<EOF>"


# ================= COMMENTS =================

def test_011():
    """Line comment"""
    assert Tokenizer("// comment").get_tokens_as_string() == "<EOF>"


def test_012():
    """Block comment"""
    assert Tokenizer("/* comment */").get_tokens_as_string() == "<EOF>"


def test_013():
    """Block comment followed by code"""
    assert Tokenizer("/* comment */x").get_tokens_as_string() == "x,<EOF>"


# ================= OPERATORS & SEPARATORS =================

def test_014():
    """Arithmetic and logical operators"""
    source = "a&&b||c"
    assert Tokenizer(source).get_tokens_as_string() == "a,&&,b,||,c,<EOF>"


def test_015():
    """Unary and binary operators"""
    source = "a--b"
    assert Tokenizer(source).get_tokens_as_string() == "a,--,b,<EOF>"


def test_016():
    """Assignment expression"""
    source = "x = 5 + 3 * 2;"
    assert Tokenizer(source).get_tokens_as_string() == "x,=,5,+,3,*,2,;,<EOF>"


def test_017():
    """Parenthesized expression"""
    source = "(a+b)*c"
    assert Tokenizer(source).get_tokens_as_string() == "(,a,+,b,),*,c,<EOF>"


# ================= MIXED =================

def test_018():
    """Function call"""
    source = 'printString("Hello");'
    assert Tokenizer(source).get_tokens_as_string() == "printString,(,Hello,),;,<EOF>"


def test_019():
    """Identifier starting with underscore"""
    assert Tokenizer("_9abc").get_tokens_as_string() == "_9abc,<EOF>"


def test_020():
    """Invalid identifier split"""
    assert Tokenizer("123_456").get_tokens_as_string() == "123,_456,<EOF>"


# ================= ERRORS =================

def test_021():
    """Illegal escape"""
    source = '"hello\\x"'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: hello\\x"


def test_022():
    """Unclosed string"""
    source = '"hello'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: hello"


def test_023():
    """Unclosed string due to newline"""
    source = '"abc\nxyz"'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: abc"


def test_024():
    """Error character"""
    assert Tokenizer("@").get_tokens_as_string() == "Error Token @"

# ================= MORE IDENTIFIERS =================

def test_025():
    assert Tokenizer("a1 b2 c3").get_tokens_as_string() == "a1,b2,c3,<EOF>"

def test_026():
    assert Tokenizer("A_B_C").get_tokens_as_string() == "A_B_C,<EOF>"

def test_027():
    assert Tokenizer("__init__").get_tokens_as_string() == "__init__,<EOF>"

def test_028():
    assert Tokenizer("_").get_tokens_as_string() == "_,<EOF>"

def test_029():
    assert Tokenizer("xYz123").get_tokens_as_string() == "xYz123,<EOF>"


# ================= NUMBERS =================

def test_030():
    assert Tokenizer("0").get_tokens_as_string() == "0,<EOF>"

def test_031():
    assert Tokenizer("1000000").get_tokens_as_string() == "1000000,<EOF>"

def test_032():
    assert Tokenizer("1e10").get_tokens_as_string() == "1e10,<EOF>"

def test_033():
    assert Tokenizer("1E-10").get_tokens_as_string() == "1E-10,<EOF>"

def test_034():
    assert Tokenizer("10.").get_tokens_as_string() == "10.,<EOF>"

def test_035():
    assert Tokenizer("0.0").get_tokens_as_string() == "0.0,<EOF>"

def test_036():
    assert Tokenizer("00").get_tokens_as_string() == "00,<EOF>"

def test_037():
    assert Tokenizer("5e+2").get_tokens_as_string() == "5e+2,<EOF>"

def test_038():
    assert Tokenizer("7.89E3").get_tokens_as_string() == "7.89E3,<EOF>"


# ================= STRINGS =================

def test_039():
    assert Tokenizer('""').get_tokens_as_string() == ",<EOF>"

def test_040():
    assert Tokenizer('" "').get_tokens_as_string() == " ,<EOF>"

def test_041():
    assert Tokenizer('"abc\\tdef"').get_tokens_as_string() == "abc\\tdef,<EOF>"

def test_042():
    assert Tokenizer('"abc\\rdef"').get_tokens_as_string() == "abc\\rdef,<EOF>"

def test_043():
    assert Tokenizer('"abc\\\\def"').get_tokens_as_string() == "abc\\\\def,<EOF>"

def test_044():
    assert Tokenizer('"12345"').get_tokens_as_string() == "12345,<EOF>"

def test_045():
    assert Tokenizer('"!@#$%"').get_tokens_as_string() == "!@#$%,<EOF>"


# ================= COMMENTS =================

def test_046():
    assert Tokenizer("//").get_tokens_as_string() == "<EOF>"

def test_047():
    assert Tokenizer("/* */").get_tokens_as_string() == "<EOF>"

def test_048():
    assert Tokenizer("/* comment \n still comment */").get_tokens_as_string() == "<EOF>"

def test_049():
    assert Tokenizer("x/*comment*/y").get_tokens_as_string() == "x,y,<EOF>"

def test_050():
    assert Tokenizer("// comment \n x").get_tokens_as_string() == "x,<EOF>"


# ================= OPERATORS =================

def test_051():
    assert Tokenizer("+ - * / %").get_tokens_as_string() == "+,-,*,/,%,<EOF>"

def test_052():
    assert Tokenizer("== != < > <= >=").get_tokens_as_string() == "==,!=,<,>,<=,>=,<EOF>"

def test_053():
    assert Tokenizer("=").get_tokens_as_string() == "=,<EOF>"

def test_054():
    assert Tokenizer("!").get_tokens_as_string() == "!,<EOF>"

def test_055():
    assert Tokenizer("&&").get_tokens_as_string() == "&&,<EOF>"

def test_056():
    assert Tokenizer("||").get_tokens_as_string() == "||,<EOF>"

def test_057():
    assert Tokenizer("++").get_tokens_as_string() == "++,<EOF>"

def test_058():
    assert Tokenizer("--").get_tokens_as_string() == "--,<EOF>"


# ================= SEPARATORS =================

def test_059():
    assert Tokenizer("()").get_tokens_as_string() == "(,),<EOF>"

def test_060():
    assert Tokenizer("{}").get_tokens_as_string() == "{,},<EOF>"

def test_062():
    assert Tokenizer(", ;").get_tokens_as_string() == ",,;,<EOF>"


# ================= MIXED EXPRESSIONS =================

def test_063():
    assert Tokenizer("a=1").get_tokens_as_string() == "a,=,1,<EOF>"

def test_064():
    assert Tokenizer("a=b+c").get_tokens_as_string() == "a,=,b,+,c,<EOF>"

def test_065():
    assert Tokenizer("x=y*z+2").get_tokens_as_string() == "x,=,y,*,z,+,2,<EOF>"

def test_066():
    assert Tokenizer("if(a>b) return a;").get_tokens_as_string() == "if,(,a,>,b,),return,a,;,<EOF>"

def test_067():
    assert Tokenizer("while(x<10)x=x+1;").get_tokens_as_string() == "while,(,x,<,10,),x,=,x,+,1,;,<EOF>"

def test_068():
    assert Tokenizer("foo(1,2,3)").get_tokens_as_string() == "foo,(,1,,,2,,,3,),<EOF>"

def test_070():
    assert Tokenizer("obj.field").get_tokens_as_string() == "obj,.,field,<EOF>"


# ================= ERRORS =================

def test_071():
    assert Tokenizer("@").get_tokens_as_string() == "Error Token @"

def test_072():
    assert Tokenizer("#").get_tokens_as_string() == "Error Token #"

def test_073():
    assert Tokenizer("$").get_tokens_as_string() == "Error Token $"

def test_074():
    assert Tokenizer('"abc\\z"').get_tokens_as_string() == "Illegal Escape In String: abc\\z"

def test_076():
    assert Tokenizer('"abc\n').get_tokens_as_string() == "Unclosed String: abc"

def test_078():
    assert Tokenizer("*/").get_tokens_as_string() == "*,/,<EOF>"


# ================= EDGE CASES =================

def test_079():
    assert Tokenizer(" ").get_tokens_as_string() == "<EOF>"

def test_080():
    assert Tokenizer("\n\t").get_tokens_as_string() == "<EOF>"

def test_081():
    assert Tokenizer("a/*c*/").get_tokens_as_string() == "a,<EOF>"

def test_082():
    assert Tokenizer("/*c*/a").get_tokens_as_string() == "a,<EOF>"

def test_083():
    assert Tokenizer("a//c").get_tokens_as_string() == "a,<EOF>"

def test_084():
    assert Tokenizer("1+2//3").get_tokens_as_string() == "1,+,2,<EOF>"


# ================= STRESS TOKEN SPLIT =================

def test_085():
    assert Tokenizer("a+++b").get_tokens_as_string() == "a,++,+,b,<EOF>"

def test_086():
    assert Tokenizer("a---b").get_tokens_as_string() == "a,--,-,b,<EOF>"

def test_087():
    assert Tokenizer("a==b").get_tokens_as_string() == "a,==,b,<EOF>"

def test_088():
    assert Tokenizer("a!=b").get_tokens_as_string() == "a,!=,b,<EOF>"

def test_089():
    assert Tokenizer("a<=b").get_tokens_as_string() == "a,<=,b,<EOF>"

def test_090():
    assert Tokenizer("a>=b").get_tokens_as_string() == "a,>=,b,<EOF>"


# ================= FINAL =================

def test_091():
    assert Tokenizer("return;").get_tokens_as_string() == "return,;,<EOF>"

def test_092():
    assert Tokenizer("break;").get_tokens_as_string() == "break,;,<EOF>"

def test_093():
    assert Tokenizer("continue;").get_tokens_as_string() == "continue,;,<EOF>"

def test_094():
    assert Tokenizer("int x;").get_tokens_as_string() == "int,x,;,<EOF>"

def test_095():
    assert Tokenizer("float y;").get_tokens_as_string() == "float,y,;,<EOF>"

def test_096():
    assert Tokenizer("string s;").get_tokens_as_string() == "string,s,;,<EOF>"

def test_097():
    assert Tokenizer("void f(){}").get_tokens_as_string() == "void,f,(,),{,},<EOF>"

def test_098():
    assert Tokenizer("struct A{}").get_tokens_as_string() == "struct,A,{,},<EOF>"

def test_099():
    assert Tokenizer("switch(x){}").get_tokens_as_string() == "switch,(,x,),{,},<EOF>"

def test_100():
    assert Tokenizer("case 1:").get_tokens_as_string() == "case,1,:,<EOF>"

def test_101():
    assert Tokenizer("default:").get_tokens_as_string() == "default,:,<EOF>"

def test_102():
    assert Tokenizer("for(i=0;i<10;i++)").get_tokens_as_string() == "for,(,i,=,0,;,i,<,10,;,i,++,),<EOF>"

def test_103():
    assert Tokenizer("if(x){}else{}").get_tokens_as_string() == "if,(,x,),{,},else,{,},<EOF>"
# ========== Simple Test Cases (10 types) ==========
def test_keyword_auto():
    """1. Keyword"""
    tokenizer = Tokenizer("auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_operator_assign():
    """2. Operator"""
    tokenizer = Tokenizer("=")
    assert tokenizer.get_tokens_as_string() == "=,<EOF>"


def test_separator_semi():
    """3. Separator"""
    tokenizer = Tokenizer(";")
    assert tokenizer.get_tokens_as_string() == ";,<EOF>"


def test_integer_single_digit():
    """4. Integer literal"""
    tokenizer = Tokenizer("5")
    assert tokenizer.get_tokens_as_string() == "5,<EOF>"


def test_float_decimal():
    """5. Float literal"""
    tokenizer = Tokenizer("3.14")
    assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"


def test_string_simple():
    """6. String literal"""
    tokenizer = Tokenizer('"hello"')
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


def test_identifier_simple():
    """7. Identifier"""
    tokenizer = Tokenizer("x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"


def test_line_comment():
    """8. Line comment"""
    tokenizer = Tokenizer("// This is a comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_integer_in_expression():
    """9. Mixed: integers and operator"""
    tokenizer = Tokenizer("5+10")
    assert tokenizer.get_tokens_as_string() == "5,+,10,<EOF>"


def test_complex_expression():
    """10. Complex: variable declaration"""
    tokenizer = Tokenizer("auto x = 5 + 3 * 2;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,*,2,;,<EOF>"
