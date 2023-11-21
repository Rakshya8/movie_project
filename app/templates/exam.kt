class Contact(val id: Int, val email: String)
fun main(){
    val customer = Contact(1, "abc@fsad.com")
    customer.email = "abc00@fsad.com"
}

