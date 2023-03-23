"use strict";

function project_filters(){
    const label = document.querySelectorAll('label');
    const filter_labels = 'country, region, status, type, validator, sub-type';

    label.forEach(e => {
        const term = e.textContent.slice(0, -1).toLowerCase()
        
        if (filter_labels.includes(term)) {
            e.classList.add('collapse-btn')
            e.classList.add('collapsed-list')
            const wrapper = document.querySelector(`.${term}-wrapper`);
            term != 'status' ? wrapper.classList.add('collapsed') : null;
            term != 'status' ? e.classList.remove('collapsed-list') : null;

            e.addEventListener('click', function(){
                wrapper.classList.toggle('collapsed');
                e.classList.toggle('collapsed-list')
            })
        }
    })

    const form = document.querySelector('.filters-form')
    const clear_btn = document.querySelector('.clear-filter-btn')

    form.addEventListener('submit', function(){
        clear_btn.classList.remove('d-none')
    })
}

project_filters()
