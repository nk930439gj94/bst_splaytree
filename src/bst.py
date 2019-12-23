import sys
import queue
 
class node:
    def __init__(self, data, left=None, right=None, inorder=None):
        self.left = left
        self.right = right
        self.data = data

    def insert(self, data):
        if data <= self.data:
            if not self.left:
                self.left = node(data)
            else:
                self.left.insert(data)
        else:
            if not self.right:
                self.right = node(data)
            else:
                self.right.insert(data)

class BST:
    def __init__(self, filename):
        self.root = None

        self._read(filename)
        self.prep_file = open( '../output/BTree_PRep.txt', 'w' )
        self.tree_file = open( '../output/BTree.txt', 'w' )
        self.boundary_file = open( '../output/BTree_boundary.txt', 'w' )


    def _read(self, filename):
        inputfile = open(filename, 'r')
        s = inputfile.read()
        self.trees = [ [ int(j) for j in i.split() ] for i in s.splitlines() ]

    def nTree(self):
        return len( self.trees )

    def insert_all(self, i):
        for d in self.trees[i]:
            self._insert(d)

    def _insert(self, data):
        if not self.root:
            self.root = node(data)
        else:
            self.root.insert(data)

    def remove_all(self):
        self.root = None
    
    def build_inorder(self):
        self.height = 0
        if self.root:
            self._build_inorder(self.root, 0, 0)

    def _build_inorder(self, n, i, l):
        if l > self.height:
            self.height = l
        if n.left:
            j = self._build_inorder(n.left, i, l+1)
        else:
            j = i
        n.inorder = j
        if n.right:
            k = self._build_inorder(n.right, j+1, l+1)
        else:
            k = j+1
        return k

    def Prep(self):
        p = ''
        if self.root:
            p = self._Prep(self.root)
        self.prep_file.write( p + '\r\n' )

    def _Prep(self, n):
        left = right = '-'
        if n.left :
            left = self._Prep(n.left)
        if n.right:
            right = self._Prep(n.right)
        if left == right == '-':
            return str(n.data)
        else:
            return str(n.data) + '(' + left + '\u00a0' + right + ')'

    def Btree(self):
        ret = ''
        self.build_inorder()
        q = queue.Queue()
        q.put(self.root)
        q.put(None)
        pos = 0
        while True:
            n = q.get()
            if not n:
                while ret[-1] == '\u00a0':
                    ret = ret[:-1]
                if q.empty():
                    break
                pos = 0
                q.put(None)
                n = q.get()
                ret += '\r\n'
            ret += ( 3 * n.inorder - pos)*'\u00a0' + "{:\u00a0<3}".format(n.data)
            pos = 3 * n.inorder + 3
            if n.left:
                q.put(n.left)
            if n.right:
                q.put(n.right)
        self.tree_file.write( ret + '\r\n' )
        
    def boudary(self):
        a = (self.height + 1) * [None]
        self._boundary(self.root, 0, a)
        self.boundary_file.write( '\u00a0'.join( map(str,a) ) + '\r\n' )

    def _boundary(self, n, l, a):
        if a[self.height] != None:
            return
        if a[l] is None:
            a[l] = n.data
        if n.left:
            self._boundary(n.left, l+1, a)
        if n.right:
            self._boundary(n.right, l+1, a)




if __name__ == '__main__':
    bst = BST( sys.argv[1] )
    for i in range(bst.nTree()):
        bst.remove_all()
        bst.insert_all(i)
        bst.Prep()
        bst.Btree()
        bst.boudary()