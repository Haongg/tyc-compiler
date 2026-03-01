import pytest
from tests.utils import Tokenizer
from src.grammar import lexererr

def test_fragment_not_escaped():
    """Test lỗi Unclosed String khi kết thúc bằng backslash lẻ loi"""
    source = """ "hello \\ \n " """
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: hello \\"

def test_float_literal_array_index():
    """Test float trong ngữ cảnh mảng"""
    source = "vals[0.5]"
    expected = "vals,Error Token ["
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_leading_dot_with_exponent():
    """Test float dạng .99e2"""
    source = ".99e2"
    expected = ".99e2,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_trailing_dot_with_exponent():
    """Test float dạng 42.e5"""
    source = "42.e5"
    expected = "42.e5,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_001():
    source = """\t\r\n
    /* This is a block comment so // has no meaning here */
    """
    assert Tokenizer(source).get_tokens_as_string() == "<EOF>"

def test_002():
    # Ký tự lạ vẫn phải báo lỗi (Strict checking)
    source = "@"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token @"

def test_003():
    source = "auto auto1"
    assert Tokenizer(source).get_tokens_as_string() == "auto,auto1,<EOF>"

def test_004():
    source = "+ ++"
    assert Tokenizer(source).get_tokens_as_string() == "+,++,<EOF>"

def test_005():
    source = "aa123"
    assert Tokenizer(source).get_tokens_as_string() == "aa123,<EOF>"

def test_006():
    source = "0   100   255   2500   -45"
    assert Tokenizer(source).get_tokens_as_string() == "0,100,255,2500,-,45,<EOF>"

def test_007():
    source = "0.0   3.14   -2.5   1.23e4   5.67E-2   1.   .5"
    assert Tokenizer(source).get_tokens_as_string() == "0.0,3.14,-,2.5,1.23e4,5.67E-2,1.,.5,<EOF>"

def test_008():
    source = """
    "This is a string containing tab \\t"
    "He asked me: \\"Where is John?\\""
    """
    # MODIFIED: Bỏ dấu ngoặc kép bao quanh token string
    # Token 1: This is a string containing tab \t
    # Token 2: He asked me: \"Where is John?\"
    expected = 'This is a string containing tab \\t,He asked me: \\"Where is John?\\",<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
    source = """
    "This is a string \n containing tab \\t"
    """
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: This is a string "

def test_010():
    source = """
    "This is a string \\z containing tab \\t"
    """
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: This is a string \\z"

def test_011():
    source = "if else while for do"
    assert Tokenizer(source).get_tokens_as_string() == "if,else,while,for,do,<EOF>"

def test_012():
    source = "break continue return void"
    assert Tokenizer(source).get_tokens_as_string() == "break,continue,return,void,<EOF>"

def test_013():
    source = "int float bool string"
    assert Tokenizer(source).get_tokens_as_string() == "int,float,bool,string,<EOF>"

def test_014():
    source = "true false"
    assert Tokenizer(source).get_tokens_as_string() == "true,false,<EOF>"


#!!
def test_015():
    source = "ifElse"
    assert Tokenizer(source).get_tokens_as_string() == "ifElse,<EOF>"

def test_016():
    source = "IF ELSE"
    assert Tokenizer(source).get_tokens_as_string() == "IF,ELSE,<EOF>"

def test_017():
    source = "+ - * / %"
    assert Tokenizer(source).get_tokens_as_string() == "+,-,*,/,%,<EOF>"

def test_018():
    source = "! && ||"
    assert Tokenizer(source).get_tokens_as_string() == "!,&&,||,<EOF>"

def test_019():
    source = "== != < > <= >="
    assert Tokenizer(source).get_tokens_as_string() == "==,!=,<,>,<=,>=,<EOF>"

def test_020():
    source = "= += -="
    assert Tokenizer(source).get_tokens_as_string() == "=,+,=,-,=,<EOF>"

def test_021():
    source = "( ) { } [ ]"
    assert Tokenizer(source).get_tokens_as_string() == "(,),{,},Error Token ["

def test_022():
    source = ", ; ."
    assert Tokenizer(source).get_tokens_as_string() == ",,;,.,<EOF>"

def test_023():
    source = "a+b"
    assert Tokenizer(source).get_tokens_as_string() == "a,+,b,<EOF>"

def test_024():
    source = "a>=b"
    assert Tokenizer(source).get_tokens_as_string() == "a,>=,b,<EOF>"
    
def test_025():
    source = "x-1"
    assert Tokenizer(source).get_tokens_as_string() == "x,-,1,<EOF>"

def test_026():
    source = "abc ABC aBc"
    assert Tokenizer(source).get_tokens_as_string() == "abc,ABC,aBc,<EOF>"

def test_027():
    source = "a123 _abc _123"
    assert Tokenizer(source).get_tokens_as_string() == "a123,_abc,_123,<EOF>"

def test_028():
    source = "variable_name camelCase PascalCase"
    assert Tokenizer(source).get_tokens_as_string() == "variable_name,camelCase,PascalCase,<EOF>"

def test_029():
    source = "__init__"
    assert Tokenizer(source).get_tokens_as_string() == "__init__,<EOF>"

def test_030():
    source = "get2"
    assert Tokenizer(source).get_tokens_as_string() == "get2,<EOF>"

def test_031():
    source = "0 00 007" 
    assert Tokenizer(source).get_tokens_as_string() == "0,00,007,<EOF>"

def test_032():
    source = "1234567890"
    assert Tokenizer(source).get_tokens_as_string() == "1234567890,<EOF>"

def test_033():
    source = "1.23 0.00"
    assert Tokenizer(source).get_tokens_as_string() == "1.23,0.00,<EOF>"

def test_034():
    source = ".5 .001"
    assert Tokenizer(source).get_tokens_as_string() == ".5,.001,<EOF>"

def test_035():
    source = "1. 123."
    assert Tokenizer(source).get_tokens_as_string() == "1.,123.,<EOF>"

def test_036():
    source = "1e10 1E10"
    assert Tokenizer(source).get_tokens_as_string() == "1e10,1E10,<EOF>"

def test_037():
    source = "1.2e-3 0.5E+2"
    assert Tokenizer(source).get_tokens_as_string() == "1.2e-3,0.5E+2,<EOF>"

def test_038():
    source = "-123 -1.5"
    assert Tokenizer(source).get_tokens_as_string() == "-,123,-,1.5,<EOF>"

def test_039():
    source = "100;"
    assert Tokenizer(source).get_tokens_as_string() == "100,;,<EOF>"

def test_040():
    source = "1+2"
    assert Tokenizer(source).get_tokens_as_string() == "1,+,2,<EOF>"

def test_041():
    source = '""'
    # MODIFIED: Chuỗi rỗng "" thì nội dung là rỗng. Kết quả là dấu phẩy ngăn cách EOF
    assert Tokenizer(source).get_tokens_as_string() == ',<EOF>'

def test_042():
    source = '"Hello World"'
    # MODIFIED: Bỏ ngoặc kép
    assert Tokenizer(source).get_tokens_as_string() == 'Hello World,<EOF>'

def test_043():
    source = '"123 !@#"'
    # MODIFIED: Bỏ ngoặc kép
    assert Tokenizer(source).get_tokens_as_string() == '123 !@#,<EOF>'

def test_044():
    source = "\"It's ok\""
    # MODIFIED: Bỏ ngoặc kép
    assert Tokenizer(source).get_tokens_as_string() == "It's ok,<EOF>"

def test_045():
    source = r'"Say \"Hi\""' 
    # MODIFIED: Bỏ ngoặc kép ngoài cùng
    assert Tokenizer(source).get_tokens_as_string() == r'Say \"Hi\",<EOF>'

def test_046():
    source = r'"Path \\ to \\ file"'
    # MODIFIED: Bỏ ngoặc kép ngoài cùng
    assert Tokenizer(source).get_tokens_as_string() == r'Path \\ to \\ file,<EOF>'

def test_047():
    source = r'"Line1\nLine2"'
    # MODIFIED
    assert Tokenizer(source).get_tokens_as_string() == r'Line1\nLine2,<EOF>'

def test_048():
    source = r'"Tab\tSep"'
    # MODIFIED
    assert Tokenizer(source).get_tokens_as_string() == r'Tab\tSep,<EOF>'

def test_049():
    source = r'"\b\f\r\n\t\"\\"'
    # MODIFIED
    assert Tokenizer(source).get_tokens_as_string() == r'\b\f\r\n\t\"\\,<EOF>'

def test_050():
    source = '"str1" "str2"'
    # MODIFIED: str1 và str2 không có ngoặc, ngăn cách bởi dấu phẩy
    assert Tokenizer(source).get_tokens_as_string() == 'str1,str2,<EOF>'

def test_051():
    source = "   \t  \n  123"
    assert Tokenizer(source).get_tokens_as_string() == "123,<EOF>"

#!!
def test_052():
    source = "// Comment line\n123"
    assert Tokenizer(source).get_tokens_as_string() == "123,<EOF>"

def test_053():
    source = "/* Block Comment */ 123"
    assert Tokenizer(source).get_tokens_as_string() == "123,<EOF>"

def test_054():
    source = "1 /* comment */ 2"
    assert Tokenizer(source).get_tokens_as_string() == "1,2,<EOF>"

def test_055():
    source = """
    /* Multi
       Line
       Comment */
    var
    """
    assert Tokenizer(source).get_tokens_as_string() == "var,<EOF>"

def test_056():
    source = "1 // comment at eof"
    assert Tokenizer(source).get_tokens_as_string() == "1,<EOF>"

def test_057():
    source = "// comment with * inside"
    assert Tokenizer(source).get_tokens_as_string() == "<EOF>"

def test_058():
    source = "/* comment with // inside */"
    assert Tokenizer(source).get_tokens_as_string() == "<EOF>"

def test_059():
    source = "/** Doc comment */"
    assert Tokenizer(source).get_tokens_as_string() == "<EOF>"

def test_060():
    source = "// !@#$%^&*()"
    assert Tokenizer(source).get_tokens_as_string() == "<EOF>"

def test_061():
    source = "#"
    # Giữ nguyên check lỗi ký tự lạ
    assert Tokenizer(source).get_tokens_as_string() == "Error Token #"

def test_062():
    source = "$"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token $"

def test_063():
    source = "~"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token ~"

def test_064():
    source = "`"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token `"

def test_065():
    source = "?"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token ?"

def test_066():
    source = "int a = @;"
    assert Tokenizer(source).get_tokens_as_string() == "int,a,=,Error Token @"

def test_067():
    source = '"Unclosed at EOF'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: Unclosed at EOF"

def test_068():
    source = '"Line1\nLine2"'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: Line1"

def test_069():
    source = '"Empty unclosed'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: Empty unclosed"

def test_070():
    source = r'"\a"'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: \\a"

def test_071():
    source = r'"\c"'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: \\c"

def test_072():
    source = r'"\x"'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: \\x"

def test_073():
    source = r'"Escape at end \"' 
    assert Tokenizer(source).get_tokens_as_string() == r'Unclosed String: Escape at end \"'

def test_074():
    source = r'"Normal string \k error"'
    assert Tokenizer(source).get_tokens_as_string() == r'Illegal Escape In String: Normal string \k'

def test_075():
    source = "int main() { return 0; }"
    assert Tokenizer(source).get_tokens_as_string() == "int,main,(,),{,return,0,;,},<EOF>"

def test_076():
    source = "float x = 1.5 + 2.0;"
    assert Tokenizer(source).get_tokens_as_string() == "float,x,=,1.5,+,2.0,;,<EOF>"

def test_077():
    source = "if (x > 10) { y = x * 2; }"
    assert Tokenizer(source).get_tokens_as_string() == "if,(,x,>,10,),{,y,=,x,*,2,;,},<EOF>"

def test_078():
    source = "string s = \"hello\";"
    # MODIFIED: "hello" -> hello
    assert Tokenizer(source).get_tokens_as_string() == 'string,s,=,hello,;,<EOF>'

def test_079():
    source = "a[i] = b[i] + 1;"
    assert Tokenizer(source).get_tokens_as_string() == "a,Error Token ["

def test_080():
    source = "func(a, b);"
    assert Tokenizer(source).get_tokens_as_string() == "func,(,a,,,b,),;,<EOF>"

def test_081():
    source = "/* header */ int x;"
    assert Tokenizer(source).get_tokens_as_string() == "int,x,;,<EOF>"

def test_082():
    source = "x++; y--;"
    assert Tokenizer(source).get_tokens_as_string() == "x,++,;,y,--,;,<EOF>"

def test_083():
    source = "val = -x;"
    assert Tokenizer(source).get_tokens_as_string() == "val,=,-,x,;,<EOF>"

def test_084():
    source = "bool flag = true;"
    assert Tokenizer(source).get_tokens_as_string() == "bool,flag,=,true,;,<EOF>"

def test_085():
    source = "for (int i=0; i<10; i=i+1)"
    assert Tokenizer(source).get_tokens_as_string() == "for,(,int,i,=,0,;,i,<,10,;,i,=,i,+,1,),<EOF>"

def test_086():
    source = "if(true)x=1;" 
    assert Tokenizer(source).get_tokens_as_string() == "if,(,true,),x,=,1,;,<EOF>"

def test_087():
    source = "1.2.3" 
    assert Tokenizer(source).get_tokens_as_string() == "1.2,.3,<EOF>"

def test_088():
    source = "......." 
    assert Tokenizer(source).get_tokens_as_string() == ".,.,.,.,.,.,.,<EOF>"

def test_089():
    source = "++++" 
    assert Tokenizer(source).get_tokens_as_string() == "++,++,<EOF>"
    
def test_090():
    source = '"if while"'
    # MODIFIED: Bỏ ngoặc
    assert Tokenizer(source).get_tokens_as_string() == 'if while,<EOF>'

def test_091():
    source = "/* if while */"
    assert Tokenizer(source).get_tokens_as_string() == "<EOF>"

def test_092():
    source = "_"
    assert Tokenizer(source).get_tokens_as_string() == "_,<EOF>"

def test_093():
    source = "123a" 
    assert Tokenizer(source).get_tokens_as_string() == "123,a,<EOF>"

def test_094():
    source = "1e" 
    assert Tokenizer(source).get_tokens_as_string() == "1,e,<EOF>"

def test_095():
    source = "1.e2" 
    assert Tokenizer(source).get_tokens_as_string() == "1.e2,<EOF>"

def test_096():
    source = "\"\"\"" 
    # Unclosed String không bao giờ có ngoặc đóng trong thông báo lỗi
    assert Tokenizer(source).get_tokens_as_string() == ",Unclosed String: "

def test_097():
    source = "int a=1;//comment"
    assert Tokenizer(source).get_tokens_as_string() == "int,a,=,1,;,<EOF>"
    
def test_098():
    source = "int bi\u00ea\u0301n;" 
    assert Tokenizer(source).get_tokens_as_string() == "int,bi,Error Token \u00ea"

def test_099():
    source = "!!!=="
    assert Tokenizer(source).get_tokens_as_string() == "!,!,!=,=,<EOF>"

def test_100():
    source = " " * 1000
    assert Tokenizer(source).get_tokens_as_string() == "<EOF>"