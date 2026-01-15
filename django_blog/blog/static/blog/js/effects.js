// Nasłuchiwanie zdarzenia załadowania DOM - wszystkie efekty uruchamiają się po pełnym załadowaniu strony
document.addEventListener('DOMContentLoaded', function() {
  // Tworzymy animowaną sieć cząsteczek w tle strony
  createParticleNetwork();

  // Inicjalizujemy animacje pojawiania się elementów podczas przewijania strony
  initScrollAnimations();

  // Dodajemy interaktywne efekty do przycisków i kart (ripple i tilt)
  initInteractiveEffects();
});

// Funkcja tworząca animowaną sieć cząsteczek w tle strony
function createParticleNetwork() {
  // Tworzymy element canvas do rysowania animacji
  const canvas = document.createElement('canvas');
  canvas.classList.add('particle-network');
  document.body.appendChild(canvas);

  // Pobieramy kontekst 2D canvas do rysowania
  const ctx = canvas.getContext('2d');
  let particles = []; // Tablica przechowująca wszystkie cząsteczki
  const particleCount = 100; // Liczba cząsteczek w animacji

  // Funkcja dostosowująca rozmiar canvas do rozmiaru okna przeglądarki
  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  // Nasłuchujemy zdarzenia zmiany rozmiaru okna i dostosowujemy canvas
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  // Generujemy losowe cząsteczki z ich właściwościami
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width, // Losowa pozycja X
      y: Math.random() * canvas.height, // Losowa pozycja Y
      size: Math.random() * 2 + 1, // Losowy rozmiar cząsteczki (1-3px)
      speedX: Math.random() * 0.5 - 0.25, // Losowa prędkość pozioma (-0.25 do 0.25)
      speedY: Math.random() * 0.5 - 0.25, // Losowa prędkość pionowa (-0.25 do 0.25)
      color: `rgba(99, 102, 241, ${Math.random() * 0.2 + 0.1})` // Kolor z losową przezroczystością
    });
  }

  // Główna funkcja animacji wywoływana w każdej klatce
  function animate() {
    // Czyszczenie całego canvas przed narysowaniem nowej klatki
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Aktualizacja pozycji i rysowanie każdej cząsteczki
    particles.forEach(particle => {
      // Przemieszczanie cząsteczki zgodnie z jej prędkością
      particle.x += particle.speedX;
      particle.y += particle.speedY;

      // Zawijanie cząsteczek na krawędziach - jeśli wyjdzie poza ekran, pojawia się po drugiej stronie
      if (particle.x > canvas.width) particle.x = 0;
      if (particle.x < 0) particle.x = canvas.width;
      if (particle.y > canvas.height) particle.y = 0;
      if (particle.y < 0) particle.y = canvas.height;

      // Rysowanie cząsteczki jako małe koło
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      ctx.fillStyle = particle.color;
      ctx.fill();
    });

    // Rysowanie linii łączących bliskie cząsteczki (efekt sieci)
    particles.forEach((particle, i) => {
      // Sprawdzamy tylko cząsteczki po bieżącej (unikamy duplikatów)
      particles.slice(i).forEach(otherParticle => {
        // Obliczanie odległości między dwiema cząsteczkami (twierdzenie Pitagorasa)
        const dx = particle.x - otherParticle.x;
        const dy = particle.y - otherParticle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // Jeśli cząsteczki są blisko siebie (mniej niż 150px), rysujemy linię
        if (distance < 150) {
          ctx.beginPath();
          // Przezroczystość linii zależy od odległości - im dalej, tym bardziej przezroczysta
          ctx.strokeStyle = `rgba(99, 102, 241, ${0.2 * (1 - distance / 150)})`;
          ctx.lineWidth = 0.5;
          ctx.moveTo(particle.x, particle.y);
          ctx.lineTo(otherParticle.x, otherParticle.y);
          ctx.stroke();
        }
      });
    });

    // Wywołanie kolejnej klatki animacji (tworzy płynną animację ~60fps)
    requestAnimationFrame(animate);
  }

  // Uruchomienie animacji
  animate();
}

// Funkcja inicjalizująca animacje elementów podczas przewijania strony
function initScrollAnimations() {
  // Opcje dla IntersectionObserver - określają kiedy element jest "widoczny"
  const observerOptions = {
    threshold: 0.1, // Element uznawany za widoczny gdy 10% jego powierzchni jest w viewport
    rootMargin: '0px 0px -50px 0px' // Dodatkowy margines - animacja rozpocznie się 50px przed pojawieniem w viewport
  };

  // Tworzenie observera który będzie obserwował elementy
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      // Jeśli element jest widoczny (wchodzi do viewport)
      if (entry.isIntersecting) {
        // Dodajemy klasy animacji (custom.css) - efekt pojawiania się od dołu
        entry.target.classList.add('animate__animated', 'animate__fadeInUp');
        // Przestajemy obserwować element (animacja odtwarza się tylko raz)
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Znajdujemy wszystkie karty blogów i karty funkcji i obserwujemy je
  document.querySelectorAll('.blog-post.card, .feature-card').forEach(el => {
    observer.observe(el);
  });
}

// Funkcja inicjalizująca interaktywne efekty na elementach strony
function initInteractiveEffects() {
  // Dodajemy efekt ripple (fala) do wszystkich przycisków
  document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
      // Obliczamy pozycję kliknięcia względem przycisku
      const x = e.clientX - e.target.getBoundingClientRect().left;
      const y = e.clientY - e.target.getBoundingClientRect().top;

      // Tworzymy element reprezentujący falę
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      this.appendChild(ripple);

      // Usuwamy element fali po zakończeniu animacji (600ms)
      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });

  // Dodajemy efekt tilt (przechylenia 3D) do kart blogów
  document.querySelectorAll('.blog-post.card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
      // Pobieramy wymiary i pozycję karty
      const rect = this.getBoundingClientRect();
      // Obliczamy pozycję kursora względem karty
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      // Znajdujemy środek karty
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Obliczamy kąty obrotu na podstawie pozycji kursora względem środka
      // Im dalej od środka, tym większy kąt obrotu (dzielenie przez 25 redukuje efekt)
      const angleY = (x - centerX) / 25; // Obrót wokół osi Y (lewo-prawo)
      const angleX = (centerY - y) / 25; // Obrót wokół osi X (góra-dół)

      // Aplikujemy transformację 3D do karty
      this.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) translateZ(10px)`;
    });

    // Gdy kursor opuszcza kartę, resetujemy transformację
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
    });
  });
}
