"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""
    # TODO: Implement AST generation methods
    def visitProgram(self, ctx: TyCParser.ProgramContext):
        return Program([self.visit(decl) for decl in ctx.decl()])
    
    def visitDecl(self, ctx: TyCParser.DeclContext):
        if ctx.structdecl():
            return StructDecl(self.visit(ctx.structdecl()))
        return FuncDecl(self.visit(ctx.fundecl()))

    def visitVartyp(self, ctx:TyCParser.VartypContext):
        return self.visitChildren(ctx)


    def visitInitValue(self, ctx:TyCParser.InitValueContext):
        return self.visitChildren(ctx)


    def visitStructdecl(self, ctx:TyCParser.StructdeclContext):
        return StructDecl(ctx.ID().getText(), [self.visit(s) for s in ctx.structstmt()])


    def visitStructstmt(self, ctx:TyCParser.StructstmtContext):
        return 


    def visitStructtyp(self, ctx:TyCParser.StructtypContext):
        return MemberDecl(self.visit(ctx.vartyp()), ctx.ID().getText())


    def visitFundecl(self, ctx:TyCParser.FundeclContext):
        return self.visitChildren(ctx)


    def visitFunctyp(self, ctx:TyCParser.FunctypContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TyCParser#paramdecl.
    def visitParamdecl(self, ctx:TyCParser.ParamdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TyCParser#paramlist.
    def visitParamlist(self, ctx:TyCParser.ParamlistContext):
        if ctx.paramlist():
            return 


    # Visit a parse tree produced by TyCParser#param.
    def visitParam(self, ctx:TyCParser.ParamContext):
        return self.visit(ctx.paramtyp())


    # Visit a parse tree produced by TyCParser#paramtyp.
    def visitParamtyp(self, ctx:TyCParser.ParamtypContext):
        if ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        return Identifier(ctx.ID().getText())


    # Visit a parse tree produced by TyCParser#body.
    def visitBody(self, ctx:TyCParser.BodyContext):
        return [self.visit(stmt) for stmt in ctx.stmt()]


    # Visit a parse tree produced by TyCParser#stmt.
    def visitStmt(self, ctx:TyCParser.StmtContext):
        if ctx.varstmt():
            return self.visit(ctx.varstmt())
        elif ctx.blockstmt():
            return self.visit(ctx.blockstmt())
        elif ctx.ifstmt():
            return self.visit(ctx.ifstmt())
        elif ctx.whilestmt():
            return self.visit(ctx.whilestmt())
        elif ctx.forstmt():
            return self.visit(ctx.forstmt())
        elif ctx.switchstmt():
            return self.visit(ctx.switchstmt())
        elif ctx.returnstmt():
            return self.visit(ctx.returnstmt())
        elif ctx.exprstmt():
            return self.visit(ctx.exprstmt())
        elif ctx.continuestmt():
            return self.visit(ctx.continuestmt())
        elif ctx.breakstmt():
            return self.visit(ctx.breakstmt())


    # Visit a parse tree produced by TyCParser#varstmt.
    def visitVarstmt(self, ctx:TyCParser.VarstmtContext):
        return VarDecl(self.visit(ctx.vartyp()), ctx.ID().getText(), self.visit(ctx.initValue()) if ctx.initValue() else None)


    # Visit a parse tree produced by TyCParser#blockstmt.
    def visitBlockstmt(self, ctx:TyCParser.BlockstmtContext):
        return BlockStmt([self.visit(stmt) for stmt in ctx.stmt()])


    # Visit a parse tree produced by TyCParser#ifstmt.
    def visitIfstmt(self, ctx:TyCParser.IfstmtContext):
        if ctx.ELSE():
            return IfStmt(self.visit(ctx.expr()), self.visit(ctx.stmt(0)), self.visit(ctx.stmt(1)))


    # Visit a parse tree produced by TyCParser#whilestmt.
    def visitWhilestmt(self, ctx:TyCParser.WhilestmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TyCParser#forstmt.
    def visitForstmt(self, ctx:TyCParser.ForstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TyCParser#forInit.
    def visitForInit(self, ctx:TyCParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TyCParser#switchstmt.
    def visitSwitchstmt(self, ctx:TyCParser.SwitchstmtContext):
        default_case = self.visit(ctx.defaultClause()) if ctx.defaultClause() else None
        return SwitchStmt(self.visit(ctx.expr()), self.visit(ctx.switchList()), default_case)


    # Visit a parse tree produced by TyCParser#switchList.
    def visitSwitchList(self, ctx:TyCParser.SwitchListContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.switchBlock())] + self.visit(ctx.switchList())


    # Visit a parse tree produced by TyCParser#caseClause.
    def visitCaseClause(self, ctx:TyCParser.CaseClauseContext):
        return CaseStmt(self.visit(ctx.expr()), [self.visit(s) for s in ctx.stmt()])


    # Visit a parse tree produced by TyCParser#defaultClause.
    def visitDefaultClause(self, ctx:TyCParser.DefaultClauseContext):
        return DefaultStmt([self.visit(s) for s in ctx.stmt()])


    # Visit a parse tree produced by TyCParser#returnstmt.
    def visitReturnstmt(self, ctx:TyCParser.ReturnstmtContext):
        if ctx.expr():
            return ReturnStmt(self.visit(ctx.expr()))
        return ReturnStmt()


    # Visit a parse tree produced by TyCParser#exprstmt.
    def visitExprstmt(self, ctx:TyCParser.ExprstmtContext):
        return ExprStmt(self.visit(ctx.expr()))


    # Visit a parse tree produced by TyCParser#continuestmt.
    def visitContinuestmt(self, ctx:TyCParser.ContinuestmtContext):
        return ContinueStmt()


    # Visit a parse tree produced by TyCParser#breakstmt.
    def visitBreakstmt(self, ctx:TyCParser.BreakstmtContext):
        return BreakStmt()


    # Visit a parse tree produced by TyCParser#expr.
    def visitExpr(self, ctx:TyCParser.ExprContext):
        return self.visit(ctx.assignExpr())


    # Visit a parse tree produced by TyCParser#assignExpr.
    def visitAssignExpr(self, ctx:TyCParser.AssignExprContext):
        if ctx.logicOrExpr():
            return self.visit(ctx.logicOrExpr())
        else:
            return AssignExpr(self.visit(ctx.logicOrExpr()), self.visit(ctx.assignExpr()))


    # Visit a parse tree produced by TyCParser#logicOrExpr.
    def visitLogicOrExpr(self, ctx:TyCParser.LogicOrExprContext):
        if ctx.logicAndExpr():
            return self.visit(ctx.logicAndExpr())
        else:
            return BinaryOp(self.visit(ctx.logicOrExpr()), "||", self.visit(ctx.logicAndExpr()))


    # Visit a parse tree produced by TyCParser#logicAndExpr.
    def visitLogicAndExpr(self, ctx:TyCParser.LogicAndExprContext):
        if ctx.equalityExpr():
            return self.visit(ctx.equalityExpr())
        else:
            return BinaryOp(self.visit(ctx.logicAndExpr()), "&&", self.visit(ctx.equalityExpr()))


    # Visit a parse tree produced by TyCParser#equalityExpr.
    def visitEqualityExpr(self, ctx:TyCParser.EqualityExprContext):
        if ctx.relationalExpr():
            return self.visit(ctx.relationalExpr())
        elif ctx.EQ():
            return BinaryOp(self.visit(ctx.equalityExpr()), "==", self.visit(ctx.relationalExpr()))
        else:
            return BinaryOp(self.visit(ctx.equalityExpr()), "!=", self.visit(ctx.relationalExpr()))


    # Visit a parse tree produced by TyCParser#relationalExpr.
    def visitRelationalExpr(self, ctx:TyCParser.RelationalExprContext):
        if ctx.addExpr():
            return self.visit(ctx.addExpr())
        elif ctx.LT():
            return BinaryOp(self.visit(ctx.relationalExpr()), "<", self.visit(ctx.addExpr()))
        elif ctx.GT():
            return BinaryOp(self.visit(ctx.relationalExpr()), ">", self.visit(ctx.addExpr()))
        elif ctx.LE():
            return BinaryOp(self.visit(ctx.relationalExpr()), "<=", self.visit(ctx.addExpr()))
        else:
            return BinaryOp(self.visit(ctx.relationalExpr()), ">=", self.visit(ctx.addExpr()))


    # Visit a parse tree produced by TyCParser#addExpr.
    def visitAddExpr(self, ctx:TyCParser.AddExprContext):
        if ctx.mulExpr():
            return self.visit(ctx.mulExpr())
        elif ctx.PLUS():
            return BinaryOp(self.visit(ctx.addExpr()), "+", self.visit(ctx.mulExpr()))
        else:
            return BinaryOp(self.visit(ctx.addExpr()), "-", self.visit(ctx.mulExpr()))


    def visitMulExpr(self, ctx:TyCParser.MulExprContext):
        if ctx.unaryExpr():
            return self.visit(ctx.unaryExpr())
        elif ctx.MUL():
            return BinaryOp(self.visit(ctx.mulExpr()), "*", self.visit(ctx.unaryExpr()))
        elif ctx.DIV():
            return BinaryOp(self.visit(ctx.mulExpr()), "/", self.visit(ctx.unaryExpr()))
        else:
            return BinaryOp(self.visit(ctx.mulExpr()), "%", self.visit(ctx.unaryExpr()))

# unaryExpr
#     : (NOT | INCREMENT | DECREMENT | PLUS | MINUS) unaryExpr
#     | postfixExpr
#     ;
    def visitUnaryExpr(self, ctx:TyCParser.UnaryExprContext):
        if ctx.postfixExpr():
            return self.visit(ctx.postfixExpr())
        elif ctx.NOT():
            return PrefixOp("!", self.visit(ctx.unaryExpr()))
        elif ctx.INCREMENT():
            return PrefixOp("++", self.visit(ctx.unaryExpr()))
        elif ctx.DECREMENT():
            return PrefixOp("--", self.visit(ctx.unaryExpr()))
        elif ctx.PLUS():
            return PrefixOp("+", self.visit(ctx.unaryExpr()))
        else:
            return PrefixOp("-", self.visit(ctx.unaryExpr()))


    def visitPostfixExpr(self, ctx: TyCParser.PostfixExprContext):
        if ctx.primaryExpr():
            return self.visit(ctx.primaryExpr())

        operand = self.visit(ctx.postfixExpr())
        op = "++" if ctx.INCREMENT() else "--"
        return PostfixOp(op, operand)


# primaryExpr
#     : ID
#     | literal
#     | structInit
#     | LPAREN expr RPAREN
#     | primaryExpr DOT ID
#     | primaryExpr LPAREN argumentList RPAREN
#     ;
    def visitPrimaryExpr(self, ctx:TyCParser.PrimaryExprContext):
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.structInit():
            return self.visit(ctx.structInit())
        elif ctx.DOT():
            return MemberAccess(self.visit(ctx.primaryExpr(0)), ctx.ID().getText())
        elif isinstance(self.visit(ctx.primaryExpr(0)), Identifier):
            return FuncCall(self.visit(ctx.primaryExpr(0)), self.visit(ctx.argumentList()))
        return self.visit(ctx.expr())

    def visitStructInit(self, ctx:TyCParser.StructInitContext):
        return self.visit(ctx.visit(ctx.argumentList()))


    def visitArgumentList(self, ctx:TyCParser.ArgumentListContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.argumentListTail())


    # argumentListTail: COMMA expr argumentListTail |;
    def visitArgumentListTail(self, ctx:TyCParser.ArgumentListTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.argumentListTail())


    def visitLiteral(self, ctx:TyCParser.LiteralContext):
        if ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())

    pass
