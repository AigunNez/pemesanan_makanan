import Node

class Linkedlist:
    def __init__(self):
        self.head = None

    def tambahData(self, nama, jumlah):
        # Mengecek apakah pesanan dengan nama yang sama sudah ada dalam linked list
        current = self.head
        while current:
            if current.name == nama:
                current.jumlah += jumlah
                return
            current = current.next

        # Jika pesanan belum ada, tambahkan sebagai simpul baru
        new_node = Node.DataPesanan(nama, jumlah)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            
    def hapusData(self, order_name):
        if self.head is None:
            print("No orders to delete.")
        elif self.head.name == order_name:
            self.head = self.head.next
        else:
            current = self.head
            while current.next:
                if current.next.name == order_name:
                    current.next = current.next.next
                    return
                current = current.next
            print(f"Order '{order_name}' not found.")

    def ambilData(self):
        data = []
        node = self.head
        while node is not None:
            data.append([node.name, str(node.jumlah)])
            node = node.next
        print(data)
        return data

    def hitungSubTotalPesanan(self, nama_pesanan):
        total = 0
        node = self.head

        while node is not None:
            if node.name == nama_pesanan:
                total += node.jumlah
            node = node.next

        return total

    def hapusSemuaData(self):
        self.head = None