class Node
{
    int data;
    Node next;
    Node(int data)
    {
        this.data=data;
        next=null;
    }
}
class LL
{
    static Node head=null,tail;
    static void add(int k)
    {
        Node nn = new Node(k);
        if(head==null)
        {
            head=nn;
            tail=nn;
        }
    }
    
}
static void display()
{
    if(head==null)
    {
        System.out.println("list is empty");
        return;

    }
    Node temp
}

