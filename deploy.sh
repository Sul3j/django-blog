#!/bin/bash

# Kolory dla output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Rozpoczęcie deployment ===${NC}"

# Sprawdź czy jesteś w głównej gałęzi
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${RED}Błąd: Nie jesteś na gałęzi main!${NC}"
    exit 1
fi

# Pobierz najnowsze zmiany
echo -e "${YELLOW}Pobieram najnowsze zmiany...${NC}"
git pull origin main

if [ $? -ne 0 ]; then
    echo -e "${RED}Błąd podczas git pull${NC}"
    exit 1
fi

# Zatrzymaj kontenery
echo -e "${YELLOW}Zatrzymuję kontenery...${NC}"
docker-compose down

# Zbuduj obrazy
echo -e "${YELLOW}Buduję obrazy Docker...${NC}"
docker-compose build

if [ $? -ne 0 ]; then
    echo -e "${RED}Błąd podczas budowania obrazów${NC}"
    exit 1
fi

# Uruchom kontenery
echo -e "${YELLOW}Uruchamiam kontenery...${NC}"
docker-compose up -d

if [ $? -ne 0 ]; then
    echo -e "${RED}Błąd podczas uruchamiania kontenerów${NC}"
    exit 1
fi

# Poczekaj na uruchomienie bazy danych
echo -e "${YELLOW}Czekam na uruchomienie bazy danych...${NC}"
sleep 10

# Wykonaj migracje
echo -e "${YELLOW}Wykonuję migracje...${NC}"
docker-compose exec -T web python manage.py migrate

if [ $? -ne 0 ]; then
    echo -e "${RED}Błąd podczas wykonywania migracji${NC}"
    exit 1
fi

# Zbierz pliki statyczne
echo -e "${YELLOW}Zbieram pliki statyczne...${NC}"
docker-compose exec -T web python manage.py collectstatic --noinput

if [ $? -ne 0 ]; then
    echo -e "${RED}Błąd podczas zbierania plików statycznych${NC}"
    exit 1
fi

# Usuń nieużywane obrazy i kontenery
echo -e "${YELLOW}Czyszczę nieużywane zasoby Docker...${NC}"
docker system prune -f

# Sprawdź status kontenerów
echo -e "${YELLOW}Status kontenerów:${NC}"
docker-compose ps

echo -e "${GREEN}=== Deployment zakończony pomyślnie! ===${NC}"
