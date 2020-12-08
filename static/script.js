function toggleMoreProducts(id) {
	tableElement = document.getElementById(id)
	if (tableElement.style.display === "none") {
		tableElement.style.display = "block";
	} else {
		tableElement.style.display = "none";
	}
}