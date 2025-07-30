/*
	Paradigm Shift by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body');

	// Breakpoints.
		breakpoints({
			default:   ['1681px',   null       ],
			xlarge:    ['1281px',   '1680px'   ],
			large:     ['981px',    '1280px'   ],
			medium:    ['737px',    '980px'    ],
			small:     ['481px',    '736px'    ],
			xsmall:    ['361px',    '480px'    ],
			xxsmall:   [null,       '360px'    ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Hack: Enable IE workarounds.
		if (browser.name == 'ie')
			$body.addClass('is-ie');

	// Mobile?
		if (browser.mobile)
			$body.addClass('is-mobile');

	// Scrolly.
		$('.scrolly')
			.scrolly({
				offset: 100
			});

	// Polyfill: Object fit.
		if (!browser.canUse('object-fit')) {

			$('.image[data-position]').each(function() {

				var $this = $(this),
					$img = $this.children('img');

				// Apply img as background.
					$this
						.css('background-image', 'url("' + $img.attr('src') + '")')
						.css('background-position', $this.data('position'))
						.css('background-size', 'cover')
						.css('background-repeat', 'no-repeat');

				// Hide img.
					$img
						.css('opacity', '0');

			});

			$('.gallery > a').each(function() {

				var $this = $(this),
					$img = $this.children('img');

				// Apply img as background.
					$this
						.css('background-image', 'url("' + $img.attr('src') + '")')
						.css('background-position', 'center')
						.css('background-size', 'cover')
						.css('background-repeat', 'no-repeat');

				// Hide img.
					$img
						.css('opacity', '0');

			});

		}

	// Gallery.
		$('.gallery')
			.on('click', 'a', function(event) {

				var $a = $(this),
					$gallery = $a.parents('.gallery'),
					$modal = $gallery.children('.modal'),
					$modalImg = $modal.find('img'),
					href = $a.attr('href');

				// Not an image? Bail.
					if (!href.match(/\.(jpg|gif|png|mp4)$/))
						return;

				// Prevent default.
					event.preventDefault();
					event.stopPropagation();

				// Locked? Bail.
					if ($modal[0]._locked)
						return;

				// Lock.
					$modal[0]._locked = true;

				// Set src.
					$modalImg.attr('src', href);

				// Set visible.
					$modal.addClass('visible');

				// Focus.
					$modal.focus();

				// Delay.
					setTimeout(function() {

						// Unlock.
							$modal[0]._locked = false;

					}, 600);

			})
			.on('click', '.modal', function(event) {

				var $modal = $(this),
					$modalImg = $modal.find('img');

				// Locked? Bail.
					if ($modal[0]._locked)
						return;

				// Already hidden? Bail.
					if (!$modal.hasClass('visible'))
						return;

				// Stop propagation.
					event.stopPropagation();

				// Lock.
					$modal[0]._locked = true;

				// Clear visible, loaded.
					$modal
						.removeClass('loaded')

				// Delay.
					setTimeout(function() {

						$modal
							.removeClass('visible')

						setTimeout(function() {

							// Clear src.
								$modalImg.attr('src', '');

							// Unlock.
								$modal[0]._locked = false;

							// Focus.
								$body.focus();

						}, 475);

					}, 125);

			})
			.on('keypress', '.modal', function(event) {

				var $modal = $(this);

				// Escape? Hide modal.
					if (event.keyCode == 27)
						$modal.trigger('click');

			})
			.on('mouseup mousedown mousemove', '.modal', function(event) {

				// Stop propagation.
					event.stopPropagation();

			})
			.prepend('<div class="modal" tabIndex="-1"><div class="inner"><img src="" /></div></div>')
				.find('img')
					.on('load', function(event) {

						var $modalImg = $(this),
							$modal = $modalImg.parents('.modal');

						setTimeout(function() {

							// No longer visible? Bail.
								if (!$modal.hasClass('visible'))
									return;

							// Set loaded.
								$modal.addClass('loaded');

						}, 275);

					});

	// Dynamic Content Loading - Versión mejorada
	$(document).ready(function() {
		// Contenedor para el contenido dinámico
		var $dynamicContent = $('#dynamic-content');
		
		// Función mejorada para cargar contenido
		function loadContent(page) {
			// Mostrar indicador de carga
			$dynamicContent.html('<div class="loading">Cargando...</div>');
			
			// Cargar el contenido
			$.ajax({
				url: page,
				dataType: 'html',
				success: function(data) {
					// Parsear el HTML recibido
					var $parsed = $('<div>').html(data);
					// Extraer solo el contenido del wrapper
					var content = $parsed.find('#wrapper').html();
					
					// Insertar el contenido
					$dynamicContent.html(content);
					
					// Re-inicializar componentes necesarios
					$body.removeClass('is-preload');
					if (browser.name == 'ie') $body.addClass('is-ie');
					if (browser.mobile) $body.addClass('is-mobile');
					$('.scrolly').scrolly({ offset: 100 });
					
					// Scroll suave al contenido cargado
					$('html, body').animate({
						scrollTop: $dynamicContent.offset().top
					}, 500);
				},
				error: function(xhr, status, error) {
					console.error("Error loading page: ", status, error);
					$dynamicContent.html('<div class="error">Error al cargar el contenido. Por favor intenta nuevamente.</div>');
				}
			});
		}

		// Manejar clics en los botones de navegación
		$(document).on('click', '.load-content', function(e) {
			e.preventDefault();
			var page = $(this).data('page');
			loadContent(page);
			
			// Actualizar el historial del navegador
			history.pushState({ page: page }, '', page);
		});
		
		// Manejar el botón de retroceso/avance del navegador
		$(window).on('popstate', function(e) {
			if (e.originalEvent.state && e.originalEvent.state.page) {
				loadContent(e.originalEvent.state.page);
			} else {
				// Si no hay estado, mostrar la página inicial
				$dynamicContent.empty();
			}
		});
		
		// Opcional: Cargar contenido inicial basado en la URL
		var initialPage = window.location.pathname.split('/').pop();
		if (initialPage !== 'index.html' && initialPage !== '') {
			loadContent(initialPage);
		}
	});

})(jQuery);