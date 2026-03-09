grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:
        result = super().emit()
        text = result.text
        if text.startswith('"'):
            text = text[1:]
        if text.endswith('\"'):
            text = text
        elif text.endswith('"'):
            text = text[:-1]
        if text.endswith('\n') or text.endswith('\r'):
            text = text[:-1]
        raise UncloseString(text)
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit()
        raise IllegalEscape(result.text[1:])
    elif tk == self.STRING_LIT:
        result = super().emit()
        result.text = result.text[1:-1]
        return result
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text);
    else:
        return super().emit();
}

options{
	language=Python3;
}

// ======================================================
//                 PARSER RULES
// ======================================================
program: (decl)* EOF;

decl : fundecl | structdecl;

// =========================VAR=============================
vartyp: INT | FLOAT | STRING | AUTO | ID;
initValue
    : expr
    | structInit
    ;

// =========================STRUCT=============================
structdecl: STRUCT ID LBRACE structstmt RBRACE SEMI;
structstmt: structtyp ID SEMI structstmt |;
structtyp: INT | STRING | FLOAT | ID;

// =========================FUNCTION=============================
fundecl: (functyp |) ID paramdecl body;
functyp: INT | VOID | FLOAT | STRING | ID;

paramdecl: LPAREN paramlist RPAREN
         | LPAREN RPAREN
        ;
paramlist: param COMMA paramlist | param;
param: paramtyp ID;
paramtyp: INT | FLOAT | STRING | ID;

body: LBRACE stmt* RBRACE;
stmt
    : varstmt
    | ifstmt
    | whilestmt
    | forstmt
    | returnstmt
    | switchstmt
    | blockstmt
    | exprstmt
    | continuestmt
    | breakstmt
    ;

varstmt: vartyp ID (ASSIGN initValue)? SEMI;

blockstmt: LBRACE stmt* RBRACE;

ifstmt: IF LPAREN expr RPAREN  stmt (ELSE stmt )?;

whilestmt: WHILE LPAREN expr RPAREN stmt ;

forstmt
    : FOR LPAREN forInit? SEMI expr? SEMI expr? RPAREN
     stmt
    ;
forInit
    : vartyp ID (ASSIGN initValue)?
    | ID ASSIGN expr
    ;

switchstmt
    : SWITCH LPAREN expr RPAREN
      LBRACE switchList (defaultClause)? RBRACE
    ;
switchList: caseClause switchList |;
caseClause
    : CASE expr COLON (stmt)*
    ;
defaultClause
    : DEFAULT COLON stmt*
    ;

returnstmt: RETURN expr SEMI
          | RETURN SEMI
          ;

exprstmt: expr SEMI;

continuestmt: CONTINUE SEMI;
breakstmt: BREAK SEMI;

// --------------------- Expression ---------------------------
expr
    : assignExpr
    ;

assignExpr
    : logicOrExpr ASSIGN assignExpr
    | logicOrExpr
    ;

logicOrExpr
    : logicOrExpr OR logicAndExpr | logicAndExpr
    ;

logicAndExpr
    : logicAndExpr AND equalityExpr | equalityExpr
    ;

equalityExpr
    : equalityExpr (EQ | NE) relationalExpr | relationalExpr
    ;

relationalExpr
    : relationalExpr (LE | GE | LT |GT) addExpr | addExpr
    ;

addExpr
    : addExpr (PLUS | MINUS) mulExpr | mulExpr
    ;

mulExpr
    : mulExpr (MUL | DIV | MOD) unaryExpr | unaryExpr
    ;
unaryExpr
    : (NOT | INCREMENT | DECREMENT | PLUS | MINUS) unaryExpr
    | postfixExpr
    ;
postfixExpr
    : primaryExpr
    | postfixExpr (INCREMENT | DECREMENT)
    ;
primaryExpr
    : ID
    | literal
    | structInit
    | LPAREN expr RPAREN
    | primaryExpr DOT ID
    | primaryExpr LPAREN argumentList RPAREN
    ;
structInit: LBRACE argumentList RBRACE;
argumentList: expr argumentListTail |;
argumentListTail: COMMA expr argumentListTail |;

literal: FLOAT_LIT | INT_LIT | STRING_LIT;

// ======================================================
//                 LEXER RULES
// ======================================================
// Keywords
AUTO     : 'auto';
BREAK    : 'break';
CASE     : 'case';
CONTINUE : 'continue';
DEFAULT  : 'default';
ELSE     : 'else';
FLOAT    : 'float';
FOR      : 'for';
IF       : 'if';
INT      : 'int';
RETURN   : 'return';
STRING   : 'string';
STRUCT   : 'struct';
SWITCH   : 'switch';
VOID     : 'void';
WHILE    : 'while';

// Operators
INCREMENT: '++';
DECREMENT: '--';

PLUS     : '+';
MINUS    : '-';
MUL      : '*';
DIV      : '/';
MOD      : '%';
NOT      : '!';

AND      : '&&';
OR       : '||';

EQ       : '==';
NE       : '!=';
LE       : '<=';
GE       : '>=';
LT       : '<';
GT       : '>';

ASSIGN   : '=';
DOT      : '.';

LBRACE   : '{';
RBRACE   : '}';
LPAREN   : '(';
RPAREN   : ')';
SEMI     : ';';
COMMA    : ',';
COLON    : ':';

// Literals
// Float Literal
FLOAT_LIT : [0-9]+ '.' [0-9]* EXP?
          | '.' [0-9]+ EXP?
          | [0-9]+ EXP
          ;

// Fragment exponent
fragment EXP : [eE] [+-]? [0-9]+ ;

// Int Literal
INT_LIT : [0-9]+ ;

// String Literal
fragment ESC_SEQ     : '\\' [bfrnt"\\];
fragment NORMAL_CHAR : ~["\\\r\n];

ILLEGAL_ESCAPE : '"' (ESC_SEQ | NORMAL_CHAR)* '\\' ~[bfrnt"\\];
UNCLOSE_STRING
    : '"' (ESC_SEQ | NORMAL_CHAR)* (EOF | '\r' | '\n')
    ;

STRING_LIT : '"' (ESC_SEQ | NORMAL_CHAR)* '"';

// ID
ID : [a-zA-Z_] [a-zA-Z0-9_]* ;


// Comment
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;
LINE_COMMENT  : '//' ~[\r\n]* -> skip ;

// Whitespace (Space, Tab, Newline, Formfeed)
WS : [ \t\r\n\f]+ -> skip ;

ERROR_CHAR : . ;