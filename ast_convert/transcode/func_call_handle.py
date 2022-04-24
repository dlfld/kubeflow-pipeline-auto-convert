import ast
import sys
from _ast import Return
from typing import Any

from params_save_util import get_func_dict, get_class_def_dict


class FuncCallTransformer(ast.NodeTransformer):
    """
        目的：
            扫描传入的方法节点，
            将类中方法所调用的方法添加到类中的方法中来
            并且将这些方法这些类所需要的第三方包也引入进来
    """
    # 保存当前方法
    current_func = None
    # 存储当前方法的名字
    cur_func_name = ""
    # 保存当前方法调用的方法名
    call_func = list([])

    def visit_FunctionDef(self, node):
        # 当前方法的名字

        # self.cur_func_name = node.name

        """
        扫描方法节点
        :param node:
        :return:
        """
        self.generic_visit(node)  # 这里表示先去访问里面的children node

        """
            添加当前节点所调用的方法
            遍历
        """
        # 如果遍历到的节点不是当前节点
        # if node.name != self.cur_func_name:
        #     return node
        func_node_list = []  # 当前方法所调用方法的节点列表
        # 存储所调用方法的import节点
        import_list = []
        # 遍历当前方法调用的方法列表，检测这些方法是否在当前源文件的方法字典中，如果在的话就将方法node添加到当前方法调用的方法列表中
        func_dict = get_func_dict()
        class_def_dict = get_class_def_dict()
        # 当前方法调用了那些方法
        for func in self.call_func:
            if func in func_dict.keys():
                func_value = func_dict[func]
                called_func_node = func_value['func']
                # 在当前位置递归的扫描被调用的方法
                # recursion_get_func = RecursionGetFunc()
                # recursion_get_func.visit(copy.deepcopy(func_node['func']))
                # 节点列表中添加当前方法，但是没有递归，
                func_node_list.append(called_func_node)
                import_list += func_value['imports']
            # 如果当前方法是类定义代码的调用

            if func in class_def_dict.keys():
                class_value = class_def_dict[func]
                func_node_list.append(class_value['class'])
                import_list += class_value['imports']

        # 方法原参数的加载
        """ 
                 方法内代码的重新组合
                 self.imports 导包代码
                 func_node_list 当前方法所调用的方法的代码
                 node.body  当前方法本身的代码
        """
        node.body = list(set(import_list)) + func_node_list + node.body
        return node

    def visit_Call(self, node) -> Any:
        """
        获取方法调用的代码
        这个方法会在每一个方法定义代码扫描之前扫描
        :param node:
        :return:
        """
        self.generic_visit(node)

        if hasattr(node.func, "value"):
            # print("call_func_name value:" + node.func.value.id)
            pass
        elif hasattr(node.func, "id"):
            cal_name = node.func.id
            self.call_func.add(cal_name)
        return node
