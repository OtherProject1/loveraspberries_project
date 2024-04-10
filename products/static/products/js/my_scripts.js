function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Найти имя куки, начинающееся с переданного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function add_product_to_basket(product_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST", // Метод запроса
        url: `/ajax/add_product_to_basket/${product_id}/`, // url запроса
        data: {                 // Параметры для запроса
            'X-CSRFToken': csrftoken
        },
        success: function (response) { // Код который выполнится  для удачного запроса
            const in_basket_parent = document.getElementById(`in_basket_${response['product_id']}`)
            const in_basket_child = document.getElementById(`product_not_in_basket_${response['product_id']}`)
            const button_basket = document.getElementById('button_basket')
            button_basket.setAttribute('data-count', response['basket_counter'])
            if (response['basket_product_quantity'] == 1) {
                button_basket.classList.add('button_basket')
                console.log('kljmdlk;;Ldkl;jasKLK;')
                in_basket_parent.removeChild(in_basket_child)
                in_basket_parent.innerHTML += `<div id="product_in_basket_${response['product_id']}" style="background-color: rgba(51, 56, 124, 0.1); width: max-content; border-radius: 5px;">
                                                    <button style="border: none; background: none; padding: 0px 0px 0px 5px;"><a
                                                            style="all: unset;" onclick="minus_product_to_basket(${response['product_id']})"><i class="fa-solid fa-minus"></i></a></button>
                                                    <input id="product_${response['product_id']}_quantity" type="text"
                                                        style="width: 53px; height: 32px; font-size: 14px; font-weight: 700; border: none; background: none; padding: 0; text-align: center;"
                                                        value=${response['basket_product_quantity']} disabled>
                                                    <button style="border: none; background: none; padding: 0px 5px 0px 0px;"><a
                                                            style="all: unset;" onclick="add_product_to_basket(${response['product_id']})"><i class="fa-solid fa-plus"></i></a></button>
                                                </div>`
            } else {
                const input_quantity = document.getElementById(`product_${response['product_id']}_quantity`)
                input_quantity.value = response['basket_product_quantity']
            }
        },
        error: function (response) { // Код который выполнится  при ошибке запроса
            console.log(response);
        }

    });
}

function minus_product_to_basket(product_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST", // Метод запроса
        url: `/ajax/minus_product_to_basket/${product_id}/`, // url запроса
        data: {                 // Параметры для запроса
            'X-CSRFToken': csrftoken
        },
        success: function (response) { // Код который выполнится  для удачного запроса
            const in_basket_parent = document.getElementById(`in_basket_${response['product_id']}`);
            const in_basket_child = document.getElementById(`product_in_basket_${response['product_id']}`);
            const button_basket = document.getElementById('button_basket');
            button_basket.setAttribute('data-count', response['basket_counter']);
            if (response['basket_product_quantity'] == 0) {
                if (response['basket_counter'] == 0) {
                    button_basket.classList.remove('button_basket')
                };
                in_basket_parent.removeChild(in_basket_child);
                in_basket_parent.innerHTML += `<div id="product_not_in_basket_${response['product_id']}">
                                                    <a id="inBasket" class="btn btn-primary-link"
                                                        style="background-color: rgb(51, 56, 124); height: 32px; padding: 1px 11px 0; align-content: center;"
                                                        value="" onclick="add_product_to_basket(${response['product_id']})">В корзину</a>
                                                </div>`;
            } else {
                const input_quantity = document.getElementById(`product_${response['product_id']}_quantity`);
                input_quantity.value = response['basket_product_quantity'];
            }
        },
        error: function (response) { // Код который выполнится  при ошибке запроса
            console.log(response);
        }

    });
}

function add_product_to_basket_from_basket_page(product_id) {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST", // Метод запроса
        url: `/ajax/add_product_to_basket/${product_id}/`, // url запроса
        data: {// Параметры для запроса
            'X-CSRFToken': csrftoken
        },
        success: function (response) { // Код который выполнится  для удачного запроса
            const button_basket = document.getElementById('button_basket')
            button_basket.setAttribute('data-count', response['basket_counter'])

            const input_quantity = document.getElementById(`product_${response['product_id']}_quantity`)
            input_quantity.value = response['basket_product_quantity']

            const total_basket_quantity = document.getElementById('total_basket_quantity')
            total_basket_quantity.textContent = response['total_basket_quantity_and_cost']['basket_quantity']

            const total_basket_cost = document.getElementById('total_basket_cost')
            total_basket_cost.textContent = (Math.round(Number(response['total_basket_quantity_and_cost']['basket_cost']).toFixed(2) * 100) / 100).toFixed(2);

            const basket_product = document.getElementById(`product_in_basket_${response['product_id']}`);
            const product_sum = basket_product.querySelector('#product_sum');
            product_sum.textContent = `${response['product_sum']} р.`;
        },
        error: function (response) { // Код который выполнится  при ошибке запроса
            console.log(response);
        }

    });
}

function minus_product_to_basket_from_basket_page(product_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST", // Метод запроса
        url: `/ajax/minus_product_to_basket/${product_id}/`, // url запроса
        data: {                 // Параметры для запроса
            'X-CSRFToken': csrftoken
        },
        success: function (response) { // Код который выполнится  для удачного запроса
            const basket_product = document.getElementById(`product_in_basket_${response['product_id']}`);
            const button_basket = document.getElementById('button_basket');
            button_basket.setAttribute('data-count', response['basket_counter']);
            if (response['basket_product_quantity'] == 0) {
                if (response['basket_counter'] == 0) {
                    button_basket.classList.remove('button_basket')
                };
                const basket_parent = document.getElementById('in_basket_parent');
                basket_parent.removeChild(basket_product);
                const total_basket_quantity = document.getElementById('total_basket_quantity');
                total_basket_quantity.textContent = response['total_basket_quantity_and_cost']['basket_quantity'];
                const total_basket_cost = document.getElementById('total_basket_cost');
                total_basket_cost.textContent = Number(response['total_basket_quantity_and_cost']['basket_cost']);
            } else {
                const input_quantity = document.getElementById(`product_${response['product_id']}_quantity`);
                input_quantity.value = response['basket_product_quantity'];
                const total_basket_quantity = document.getElementById('total_basket_quantity')
                total_basket_quantity.textContent = response['total_basket_quantity_and_cost']['basket_quantity']
                const total_basket_cost = document.getElementById('total_basket_cost')
                total_basket_cost.textContent = (Math.round(Number(response['total_basket_quantity_and_cost']['basket_cost']).toFixed(2) * 100) / 100).toFixed(2);
                const product_sum = basket_product.querySelector('#product_sum');
                product_sum.textContent = `${response['product_sum']} р.`;
            }
        },
        error: function (response) { // Код который выполнится  при ошибке запроса
            console.log(response);
        }

    });
}

function delete_product_from_basket(product_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST", // Метод запроса
        url: `/ajax/delete_product_from_basket/${product_id}/`, // url запроса
        data: {                 // Параметры для запроса
            'X-CSRFToken': csrftoken
        },
        success: function (response) { // Код который выполнится  для удачного запроса
            const basket_product = document.getElementById(`product_in_basket_${response['product_id']}`);
            const button_basket = document.getElementById('button_basket');
            button_basket.setAttribute('data-count', response['basket_counter']);
            if (response['basket_counter'] == 0) {
                button_basket.classList.remove('button_basket')
            };
            const basket_parent = document.getElementById('in_basket_parent');
            basket_parent.removeChild(basket_product);
            const total_basket_quantity = document.getElementById('total_basket_quantity');
            total_basket_quantity.textContent = response['total_basket_quantity_and_cost']['basket_quantity'];
            const total_basket_cost = document.getElementById('total_basket_cost');
            total_basket_cost.textContent = Number(response['total_basket_quantity_and_cost']['basket_cost']);
        },
        error: function (response) { // Код который выполнится  при ошибке запроса
            console.log(response);
        }

    });
};

function add_product_to_favorites(product_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
                console.log('beforesend')
            }
        }
    });

    $.ajax({
        type: "POST", // Метод запроса
        url: `/ajax/ajax_add_product_to_favorites/${product_id}/`, // url запроса
        data: {                 // Параметры для запроса
            'X-CSRFToken': csrftoken
        },
        success: function (response) { // Код который выполнится  для удачного запроса
            const favorite_product = document.getElementById(`favorite_heart_${response['product_id']}`)
            if (response['add_product'] == true) {
                favorite_product.classList.remove('fa-regular');
                favorite_product.classList.add('fa-solid');
            } else {
                favorite_product.classList.remove('fa-solid');
                favorite_product.classList.add('fa-regular');
            };
        },
        error: function (response) { // Код который выполнится  при ошибке запроса
            console.log(response);
        }

    });
}


$(document).on('click', '#inBasket', function () {
    sendNotification('success', 'Товар добавлен в корзину');
});


function sendNotification(type, text) {
    let notificationBox = document.querySelector(".notification-box");
    const alerts = {
        success: {
            icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>`,
            color: "green-500"
        }
    };
    let component = document.createElement("div");
    component.className = `notific`;
    component.innerHTML = `<p>${text}</p>`;
    notificationBox.appendChild(component);
    setTimeout(() => {
        notificationBox.removeChild(component);
    }, 2700);
    //If you can do something more elegant than timeouts, please do, but i can't
};

