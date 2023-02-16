"use strict";

$(document).ready(function () {


    // preloader
    var $preloader = $('.preloader');
    if($preloader.length) {
        $preloader.delay(500).fadeOut('slow');
    }

    // options
    var breakpoints = {
        sm: 540,
        md: 720,
        lg: 960,
        xl: 1140
    };

    var $navbarCollapse = $('.navbar-main .collapse');

    // Collapse navigation
    $navbarCollapse.on('hide.bs.collapse', function () {
        var $this = $(this);
        $this.addClass('collapsing-out');
        $('html, body').css('overflow', 'initial');
    });

    $navbarCollapse.on('hidden.bs.collapse', function () {
        var $this = $(this);
        $this.removeClass('collapsing-out');
    });

    $navbarCollapse.on('shown.bs.collapse', function () {
        $('html, body').css('overflow', 'hidden');
    });

    $('.navbar-main .dropdown').on('hide.bs.dropdown', function () {
        var $this = $(this).find('.dropdown-menu');

        $this.addClass('close');

        setTimeout(function () {
            $this.removeClass('close');
        }, 200);

    });

    $(document).on('click', '.mega-dropdown', function (e) {
        e.stopPropagation();
    });

    $(document).on('click', '.navbar-nav > .dropdown', function (e) {
        e.stopPropagation();
    });

    $('.dropdown-submenu > .dropdown-toggle').click(function (e) {
        e.preventDefault();
        $(this).parent('.dropdown-submenu').toggleClass('show');
    });

    // Background images for sections
    $('[data-background]').each(function () {
        $(this).css('background-image', 'url(' + $(this).attr('data-background') + ')');
    });

    $('[data-background-color]').each(function () {
        $(this).css('background-color', $(this).attr('data-background-color'));
    });

    // Tooltip
    $('[data-toggle="tooltip"]').tooltip();

    // Popover
    $('[data-toggle="popover"]').each(function () {
        var popoverClass = '';
        if ($(this).data('color')) {
            popoverClass = 'popover-' + $(this).data('color');
        }
        $(this).popover({
            trigger: 'focus',
            template: '<div class="popover ' + popoverClass + '" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
        })
    });

    // Additional .focus class on form-groups
    $('.form-control').on('focus blur', function (e) {
        $(this).parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
    }).trigger('blur');

    var e = document.querySelector('[data-toggle="price"]');
    "undefined" != typeof CountUp && e && e.addEventListener("change", function(e) {
        ! function(e) {
            var t = e.target,
                d = t.checked,
                a = t.dataset.target,
                o = document.querySelectorAll(a);
            [].forEach.call(o, function(e) {
                var t = e.dataset.annual,
                    a = e.dataset.monthly,
                    o = e.dataset.decimals ? e.dataset.decimals : null,
                    n = e.dataset.duration ? e.dataset.duration : 1,
                    r = e.dataset.options ? JSON.parse(e.dataset.options) : null,
                    l = d ? new CountUp(e, t, a, o, n, r) : new CountUp(e, a, t, o, n, r);
                l.error ? console.error(l.error) : l.start()
            })
        }(e)
    })

    //Owl Carousel
    $('.testimonial-carousel').owlCarousel({
        loop: true,
        margin: 8,
        nav: false,
        dots: true,
        autoplay: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 1
            }
        },
    });

    // When in viewport
    $('[data-toggle="on-screen"]')[0] && $('[data-toggle="on-screen"]').onScreen({
        container: window,
        direction: 'vertical',
        doIn: function () {
            //alert();
        },
        doOut: function () {
            // Do something to the matched elements as they get off scren
        },
        tolerance: 200,
        throttle: 50,
        toggleClass: 'on-screen',
        debug: false
    });

    // Scroll to anchor with scroll animation
    $('[data-toggle="scroll"]').on('click', function (event) {
        var hash = $(this).attr('href');
        var offset = $(this).data('offset') ? $(this).data('offset') : 0;

        // Animate scroll to the selected section
        $('html, body').stop(true, true).animate({
            scrollTop: $(hash).offset().top - offset
        }, 600);

        event.preventDefault();
    });

    //Rotating Cards
    $(document).on('click', '.card-rotate .btn-rotate', function () {
        var $rotating_card_container = $(this).closest('.rotating-card-container');

        if ($rotating_card_container.hasClass('hover')) {
            $rotating_card_container.removeClass('hover');
        } else {
            $rotating_card_container.addClass('hover');
        }
    });
});
