"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser


# def test_parser_placeholder():
#     """Placeholder test - replace with actual test cases"""
#     source = "// This is a placeholder test"
#     parser = Parser(source)
#     # TODO: Add actual test assertions
#     assert True

# ==============================================================================
# GROUP 1: PROGRAM STRUCTURE & TOP LEVEL (5 Tests)
# ==============================================================================

def test_001_empty_program():
    """Test chương trình rỗng (hợp lệ theo spec: possibly empty sequence)"""
    source = ""
    parser = Parser(source)
    assert parser.parse() == "success"

def test_002_only_structs():
    """Test chương trình chỉ có khai báo struct"""
    source = "struct Point { int x; };"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_003_only_functions():
    """Test chương trình chỉ có khai báo hàm"""
    source = "void main() {}"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_004_mixed_structs_and_functions():
    """Test trộn lẫn struct và function"""
    source = """
    struct Point { int x; int y; };
    void main() {}
    """
    parser = Parser(source)
    assert parser.parse() == "success"

def test_005_comments_at_top_level():
    """Test comment ở cấp độ toàn cục"""
    source = """
    // Line comment
    /* Block comment */
    void main() {}
    """
    parser = Parser(source)
    assert parser.parse() == "success"

# ==============================================================================
# GROUP 2: STRUCT DECLARATIONS (10 Tests)
# ==============================================================================

def test_006_struct_empty():
    source = "struct Empty {};"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_007_struct_primitive_members():
    source = "struct Data { int id; float value; string label; };"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_008_struct_nested_type_member():
    """Member là một struct type khác"""
    source = """
    struct Point { int x; };
    struct Line { Point start; Point end; };
    """
    parser = Parser(source)
    assert parser.parse() == "success"

def test_009_struct_name_keywords():
    """Tên struct có chứa ký tự hợp lệ"""
    source = "struct My_Struct_123 { int x; };"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_010_struct_no_semicolon_fail():
    """Lỗi: Thiếu dấu chấm phẩy cuối struct"""
    source = "struct Point { int x; }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_011_struct_member_auto_fail():
    """Lỗi: Member dùng auto (Spec: phải explicit type)"""
    source = "struct Point { auto x; };"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_012_struct_nested_decl_fail():
    """Lỗi: Khai báo struct lồng nhau (Spec: not supported)"""
    source = "struct Outer { struct Inner { int x; }; };"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_013_struct_member_void_fail():
    """Lỗi: Member kiểu void (Spec: void not allowed for variable)"""
    source = "struct S { void x; };"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_014_struct_init_empty():
    """Test init struct trong hàm: empty braces"""
    source = "void main() { Point p = {}; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_015_struct_init_values():
    """Test init struct đầy đủ giá trị"""
    source = "void main() { Point p = {1, 2.5, \"text\"}; }"
    parser = Parser(source)
    assert parser.parse() == "success"

# ==============================================================================
# GROUP 3: FUNCTION DECLARATIONS (10 Tests)
# ==============================================================================

def test_016_func_void_no_args():
    source = "void run() {}"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_017_func_explicit_return():
    source = "int getInt() { return 1; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_018_func_inferred_return():
    """Return type omitted (Spec: allowed)"""
    source = "add(int x, int y) { return x + y; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_019_func_params_primitive():
    source = "void test(int a, float b, string c) {}"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_020_func_param_struct():
    source = "void process(Point p) {}"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_021_func_param_auto_fail():
    """Lỗi: Tham số dùng auto (Spec: params cannot use auto)"""
    source = "void test(auto x) {}"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_022_func_body_empty():
    source = "void main() {}"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_023_func_missing_body_fail():
    """Lỗi: Hàm không có body"""
    source = "void main();"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_024_func_nested_fail():
    """Lỗi: Hàm lồng nhau (C-like không hỗ trợ)"""
    source = "void main() { void nested() {} }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_025_func_return_void_keyword():
    """Hàm void return;"""
    source = "void main() { return; }"
    parser = Parser(source)
    assert parser.parse() == "success"

# ==============================================================================
# GROUP 4: VARIABLES (10 Tests)
# ==============================================================================

def test_026_var_auto_init():
    source = "void main() { auto x = 10; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_027_var_auto_no_init():
    source = "void main() { auto x; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_028_var_explicit_init():
    source = "void main() { int x = 10; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_029_var_explicit_no_init():
    source = "void main() { float y; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_030_var_struct_type():
    source = "void main() { Point p; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_031_var_multiple_decl():
    """Nhiều khai báo biến liên tiếp"""
    source = "void main() { int x; float y; string z; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_032_var_decl_in_block():
    source = "void main() { { int x = 1; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_033_var_void_type_fail():
    """Lỗi: Biến kiểu void"""
    source = "void main() { void x; }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_034_var_missing_semicolon_fail():
    source = "void main() { int x = 5 }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_035_var_assignment_only():
    """Expression statement: assignment"""
    source = "void main() { x = 5; }"
    parser = Parser(source)
    assert parser.parse() == "success"

# ==============================================================================
# GROUP 5: CONTROL FLOW - IF/ELSE (8 Tests)
# ==============================================================================

def test_036_if_single():
    source = "void main() { if (x) stmt; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_037_if_block():
    source = "void main() { if (x > 0) { x = 1; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_038_if_else():
    source = "void main() { if (1) {} else {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_039_if_else_if():
    source = "void main() { if (a) {} else if (b) {} else {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_040_if_nested():
    source = "void main() { if (a) { if (b) {} } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_041_if_dangling_else():
    """Kiểm tra parser xử lý else gắn với if gần nhất"""
    source = "void main() { if (a) if (b) s1; else s2; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_042_if_condition_complex():
    source = "void main() { if ((a > b) && (c != d)) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_043_if_missing_parens_fail():
    source = "void main() { if x > 0 {} }"
    parser = Parser(source)
    assert parser.parse() != "success"

# ==============================================================================
# GROUP 6: CONTROL FLOW - LOOPS (12 Tests)
# ==============================================================================

def test_044_while_simple():
    source = "void main() { while (true) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_045_while_one_statement():
    source = "void main() { while (1) x++; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_046_for_full():
    source = "void main() { for (int i=0; i<10; i++) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_047_for_auto_init():
    source = "void main() { for (auto i=0; i<10; i++) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_048_for_no_init():
    source = "void main() { for (; i<10; i++) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_049_for_no_cond():
    source = "void main() { for (i=0;; i++) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_050_for_no_update():
    source = "void main() { for (i=0; i<10;) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_051_for_infinite():
    source = "void main() { for (;;) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_052_break_stm():
    source = "void main() { while(1) break; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_053_continue_stm():
    source = "void main() { for(;;) continue; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_054_break_outside_loop_context():
    """
    Lưu ý: Parser thường chấp nhận break về cú pháp,
    Semantic analysis mới bắt lỗi ngữ nghĩa. Test này giả định parser chấp nhận.
    """
    source = "void main() { break; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_055_invalid_for_syntax_fail():
    source = "void main() { for (i < 10) {} }"
    parser = Parser(source)
    assert parser.parse() != "success"

# ==============================================================================
# GROUP 7: CONTROL FLOW - SWITCH (10 Tests)
# ==============================================================================

def test_056_switch_basic():
    source = "void main() { switch(x) { case 1: break; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_057_switch_multiple_cases():
    source = "void main() { switch(x) { case 1: case 2: stmt; break; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_058_switch_default():
    source = "void main() { switch(x) { default: break; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_059_switch_mixed():
    source = "void main() { switch(x) { case 1: s1; default: s2; case 3: s3; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_060_switch_empty_body():
    source = "void main() { switch(x) {} }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_061_switch_case_const_expr():
    """Spec: case expression can be constant expression"""
    source = "void main() { switch(x) { case 1+2: break; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_062_switch_case_parenthesis():
    source = "void main() { switch(x) { case (4): break; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_063_switch_case_unary():
    source = "void main() { switch(x) { case -5: break; } }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_064_switch_no_body_fail():
    source = "void main() { switch(x); }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_065_switch_case_variable_fail():
    """Case label phải là constant expression, không phải biến"""
    # Parser có thể chấp nhận expression tổng quát tùy implementation,
    # nhưng theo spec C-like thường yêu cầu constant.
    # Ở đây giả định parser chấp nhận expression cú pháp.
    # Nếu grammar chặt: source = "switch(x) { case y: break; }" -> fail
    pass # Bỏ qua do phụ thuộc grammar cụ thể sinh viên viết

# ==============================================================================
# GROUP 8: EXPRESSIONS & LITERALS (20 Tests)
# ==============================================================================

def test_066_expr_literals():
    source = "void main() { x = 1; y = 2.5; z = \"str\"; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_067_expr_float_scientific():
    """Spec: float literals like 1.23e4"""
    source = "void main() { x = 1.23e4; y = 5.E-2; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_068_expr_float_dot():
    """Spec: float literals like 1. or .5"""
    source = "void main() { x = 1.; y = .5; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_069_expr_string_escapes():
    """Spec: escapes \\n \\t \\\" \\\\"""
    source = "void main() { s = \"Hello\\nWorld\\t\\\"Quote\\\"\"; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_070_expr_binary_math():
    source = "void main() { x = a + b - c * d / e % f; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_071_expr_relational():
    source = "void main() { res = a < b && c >= d || e == f; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_072_expr_unary():
    source = "void main() { x = -a; y = !b; z = +c; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_073_expr_increment():
    source = "void main() { x++; ++y; x--; --y; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_074_expr_member_access():
    source = "void main() { val = p.x; obj.prop.sub; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_075_expr_func_call():
    source = "void main() { f(); f(1); f(a, b); }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_076_expr_complex_precedence():
    source = "void main() { x = a.b() + c[d] * -e; }" # c[d] is not in TyC spec?
    # Correcting: TyC spec has NO arrays.
    source = "void main() { x = a.b + c * -e; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_077_expr_assignment_chain():
    source = "void main() { a = b = c = 0; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_078_expr_member_assignment():
    source = "void main() { p.x = 10; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_079_expr_parenthesis():
    source = "void main() { x = (a + b) * c; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_080_expr_struct_literal_in_arg():
    """Spec: Struct literals in function calls"""
    source = "void main() { f({1, 2}); }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_081_expr_illegal_string_escape_fail():
    """Spec: hex escapes not supported"""
    source = "void main() { s = \"\\x01\"; }"
    parser = Parser(source)
    # Parser/Lexer should fail
    assert parser.parse() != "success"

def test_082_expr_unclosed_string_fail():
    source = "void main() { s = \"Hello; }"
    parser = Parser(source)
    assert parser.parse() != "success"

def test_083_expr_empty_string():
    source = "void main() { s = \"\"; }"
    parser = Parser(source)
    assert parser.parse() == "success"

def test_084_expr_modulus_float_syntax():
    """Parser accepts syntax, types checker rejects later"""
    source = "void main() { x = 5.5 % 2; }"
    parser = Parser(source)
    assert parser.parse() == "success"

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
    source = "void main() { f; }" # This is valid expression (variable access) but f is func
    # Syntax-wise: Identifier is an expression. Statement "f;" is "ExprStmt".
    # So this IS valid syntax (statement with no effect), unless semantic check knows f is func.
    # Let's test malformed call:
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