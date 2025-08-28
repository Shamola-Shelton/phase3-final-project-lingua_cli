# tests/test_structures.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.structures import DoublyLinkedList, GrammarTree
import pytest

def test_doubly_linked_list():
    dll = DoublyLinkedList()
    dll.add("word2")
    dll.add("word1")
    assert dll.search("word1") is not None
    dll.sort()
    assert dll.head.data == "word1"  # After sort: word1, word2

def test_grammar_tree():
    tree = GrammarTree()
    tree.insert("verb")
    tree.insert("noun")
    result = tree.traverse_in_order(tree.root)
    assert result == ["noun", "verb"]  # In-order: noun, verb