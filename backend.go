package main

import (
    "net/http"
    "fmt"
)


func search(w http.ResponseWriter, req *http.Request) {
    fmt.Fprintf(w, "test data")

}


func main() {
    http.HandleFunc("/api/search", search)
    http.ListenAndServe(":80", nil)
}
