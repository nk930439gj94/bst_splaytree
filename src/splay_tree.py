import sys
import queue

class node:
    def __init__(self, data, parent, left=None, right=None, inorder=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.data = data

    def insert(self, data):
        if data <= self.data:
            if not self.left:
                self.left = node(data, self)
                return self.left
            else:
                return self.left.insert(data)
        else:
            if not self.right:
                self.right = node(data, self)
                return self.right
            else:
                return self.right.insert(data)

class SplayTree:
    def __init__(self, filename):
        self.root = None

        self._read(filename)
        self.prep_file = open( '../output/STree_PRep.txt', 'w' )
        self.tree_file = open( '../output/STree.txt', 'w' )
        self.boundary_file = open( '../output/STree_boundary.txt', 'w' )


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
            n = self.root = node(data, None)
        else:
            n = self.root.insert(data)
        self.splay(n)

    def remove_all(self):
        self.root = None

    def splay(self, n):
        while n != self.root:
            self._move_up(n)

    def _move_up(self, n):
        if n == self.root:
            return
        elif n.parent == self.root:
            if n.parent.left == n:
                # l
                if n.right:
                    n.right.parent = self.root
                self.root.left = n.right
                n.right = self.root
                self.root.parent = n
                n.parent = None
                self.root = n
            else:
                # r
                if n.left:
                    n.left.parent = self.root
                self.root.right = n.left
                n.left = self.root
                self.root.parent = n
                n.parent = None
                self.root = n
        else:
            p = n.parent
            pp = n.parent.parent
            if n.parent.left == n:
                if pp.left == p:
                    # ll
                    if n.right:
                        n.right.parent = p
                    p.left = n.right
                    if p.right:
                        p.right.parent = pp
                    pp.left = p.right
                    n.right = p
                    p.parent = n
                    n.parent = pp.parent
                    if not pp.parent:
                        self.root = n
                    else:
                        if pp.parent.left == pp:
                            pp.parent.left = n
                        else:
                            pp.parent.right = n
                    p.right = pp
                    pp.parent = p

                else:
                    # rl
                    if n.right:
                        n.right.parent = p
                    p.left = n.right
                    if n.left:
                        n.left.parent = pp
                    pp.right = n.left
                    p.parent = n
                    n.right = p
                    n.parent = pp.parent
                    if not pp.parent:
                        self.root = n
                    else:
                        if pp.parent.left == pp:
                            pp.parent.left = n
                        else:
                            pp.parent.right = n
                    n.left = pp
                    pp.parent = n
            else:
                if n.parent.parent.left == n.parent:
                    # lr
                    if n.left:
                        n.left.parent = p
                    p.right = n.left
                    if n.right:
                        n.right.parent = pp
                    pp.left = n.right
                    p.parent = n
                    n.left = p
                    n.parent = pp.parent
                    if not pp.parent:
                        self.root = n
                    else:
                        if pp.parent.left == pp:
                            pp.parent.left = n
                        else:
                            pp.parent.right = n
                    n.right = pp
                    pp.parent = n
                else:
                    # rr
                    if n.left:
                        n.left.parent = p
                    p.right = n.left
                    if p.left:
                        p.left.parent = pp
                    pp.right = p.left
                    n.left = p
                    p.parent = n
                    n.parent = pp.parent
                    if not pp.parent:
                        self.root = n
                    else:
                        if pp.parent.left == pp:
                            pp.parent.left = n
                        else:
                            pp.parent.right = n
                    p.left = pp
                    pp.parent = p


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
    st = SplayTree( sys.argv[1] )
    for i in range(st.nTree()):
        st.remove_all()
        st.insert_all(i)
        st.Prep()
        st.Btree()
        st.boudary()