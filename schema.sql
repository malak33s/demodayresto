-- Création de la base de données
CREATE DATABASE IF NOT EXISTS demoday_db;
USE demoday_db;

-- Création de la table des menus
CREATE TABLE IF NOT EXISTS menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50),
    prix DECIMAL(5,2) NOT NULL,
    quantite_disponible INT NOT NULL,
    temps_preparation INT NOT NULL
);

-- Création de la table des commandes
CREATE TABLE IF NOT EXISTS commandes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_client VARCHAR(255) NOT NULL,
    date_retrait DATE NOT NULL,
    heure_retrait TIME NOT NULL,
    total DECIMAL(6,2) NOT NULL,
    details JSON NOT NULL,
    horaire VARCHAR(5) NOT NULL -- Ajout des horaires pour commandes
);

-- Insérer les plats et boissons par défaut
INSERT INTO menus (nom, description, type, prix, quantite_disponible, temps_preparation) VALUES
('Brick', 'Feuille de brik farcie et frite', 'Entrée', 2.90, 30, 20),
('Slata Méchouia', 'Salade grillée à base de poivrons, tomates et ail', 'Entrée', 3.50, 30, 15),
('Fricassée', 'Petits pains frits garnis de thon, olives, harissa', 'Plat', 1.90, 30, 10),
('Riz Djerbien', 'Riz cuit à la vapeur avec légumes et viande', 'Plat', 13.90, 30, 30),
('Nwasser', 'Pâtes traditionnelles tunisiennes avec sauce', 'Plat', 12.90, 30, 25),
('Couscous Tunisien', 'Couscous aux légumes et viande au choix', 'Plat', 16.50, 30, 40),
('Chakchouka', 'Œufs pochés dans une sauce tomate épicée', 'Plat', 10.90, 30, 20),
('Baklawa', 'Pâtisserie aux amandes et miel', 'Dessert', 3.90, 30, 10),
('Makrout', 'Gâteau semoule fourré aux dattes', 'Dessert', 2.90, 30, 15),
('Zrir', 'Mélange de graines et miel', 'Dessert', 2.90, 30, 10),
('Ice tea pêche', 'Boisson rafraîchissante à la pêche', 'Boisson', 2.00, 50, 2),
('Ice tea framboise', 'Boisson rafraîchissante à la framboise', 'Boisson', 2.00, 50, 2),
('Coca Cola Zero', 'Soda sans sucre', 'Boisson', 2.00, 50, 2),
('Coca Cola Original', 'Soda classique', 'Boisson', 2.00, 50, 2),
('Coca Cola Cherry', 'Soda goût cerise', 'Boisson', 2.00, 50, 2),
('Oasis Tropical', 'Boisson aux fruits tropicaux', 'Boisson', 2.00, 50, 2),
('Oasis Pomme, cassis, framboise', 'Boisson fruitée', 'Boisson', 2.00, 50, 2),
('Perrier', 'Eau gazeuse', 'Boisson', 2.00, 50, 2),
('Eau Abatilles', 'Eau minérale', 'Boisson', 1.50, 50, 2),
('Café arabe', 'Café oriental', 'Boisson chaude', 2.50, 50, 5),
('Thé rouge tunisien', 'Thé aux épices', 'Boisson chaude', 2.50, 50, 5),
('Espresso', 'Café serré', 'Boisson chaude', 2.50, 50, 5);
