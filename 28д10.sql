-- ==========================================
-- 1. СОЗДАНИЕ ФУНКЦИИ ДЛЯ ГЕНЕРАЦИИ СЛУЧАЙНЫХ ИМЕН
-- ==========================================
DELIMITER //

DROP FUNCTION IF EXISTS get_random_student_name//

CREATE FUNCTION get_random_student_name() 
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
    DECLARE v_random_name VARCHAR(100);
    
    -- Используем ELT и FLOOR(RAND()) для выбора из списка
    SET v_random_name = ELT(FLOOR(1 + RAND() * 5), 
        'Ivan', 'Petr', 'Anna', 'Maria', 'Sergey');
        
    RETURN v_random_name;
END//

-- ==========================================
-- 2. СОЗДАНИЕ ПРОЦЕДУРЫ ДЛЯ ЗАПОЛНЕНИЯ ТАБЛИЦЫ STUDENTS
-- ==========================================
DROP PROCEDURE IF EXISTS ps_students_insert//

CREATE PROCEDURE ps_students_insert(IN p_count INT)
BEGIN
    DECLARE v_counter INT DEFAULT 0;
    DECLARE v_student_name VARCHAR(100);
    DECLARE v_email VARCHAR(150);
    DECLARE v_group_id INT;

    -- Цикл WHILE для автоматического заполнения
    WHILE v_counter < p_count DO
        
        -- 1. Получаем случайное имя через функцию
        SET v_student_name = get_random_student_name();
        
        -- 2. Генерируем случайный ID группы (от 1 до 3)
        SET v_group_id = FLOOR(1 + RAND() * 3);
        
        -- 3. Формируем email с помощью concat()
        SET v_email = CONCAT(LOWER(v_student_name), '_', v_counter + 1, '@academy.com');

        -- 4. Запрос INSERT
        INSERT INTO students (name, email, group_id) 
        VALUES (v_student_name, v_email, v_group_id);

        -- Увеличиваем счетчик
        SET v_counter = v_counter + 1;
        
    END WHILE;

END//

DELIMITER ;

-- ==========================================
-- 3. ВЫЗОВ ПРОЦЕДУРЫ ДЛЯ ПРОВЕРКИ (Создаст 10 студентов)
-- ==========================================
CALL ps_students_insert(10);

-- Проверка результата
SELECT * FROM students;
