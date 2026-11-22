DELIMITER //

DROP PROCEDURE IF EXISTS ps_shedule_insert//

CREATE PROCEDURE ps_shedule_insert(IN p_start_date DATE, IN p_days_count INT)
BEGIN
    -- Объявляем переменные
    DECLARE v_current_date DATE;
    DECLARE v_counter INT DEFAULT 0;
    DECLARE v_lesson_id INT;
    DECLARE v_group_id INT;
    DECLARE v_teacher_id INT;

    -- Инициализируем начальную дату
    SET v_current_date = p_start_date;

    -- Цикл WHILE для автоматического заполнения таблицы
    WHILE v_counter < p_days_count DO
        
        -- Условие IF: например, заполняем только рабочие дни (пн-пт)
        -- DAYOFWEEK: 1 - Воскресенье, 2 - Понедельник ... 7 - Суббота
        IF DAYOFWEEK(v_current_date) NOT IN (1, 7) THEN
            
            -- Генерируем случайные ID (или задаем конкретные логические условия)
            -- Предполагаем, что у вас есть данные в таблицах lessons, student_group, teachers
            SET v_lesson_id = FLOOR(1 + RAND() * 5);   -- Случайный ID урока (от 1 до 5)
            SET v_group_id = FLOOR(1 + RAND() * 3);    -- Случайный ID группы (от 1 до 3)
            SET v_teacher_id = FLOOR(1 + RAND() * 4);  -- Случайный ID учителя (от 1 до 4)

            -- Запрос INSERT для добавления записи в таблицу schedule
            INSERT INTO schedule (date, lesson_id, student_group_id, teacher_id)
            VALUES (v_current_date, v_lesson_id, v_group_id, v_teacher_id);
            
        END IF;

        -- Увеличиваем дату на 1 день
        SET v_current_date = DATE_ADD(v_current_date, INTERVAL 1 DAY);
        -- Увеличиваем счетчик цикла
        SET v_counter = v_counter + 1;
        
    END WHILE;

END//

DELIMITER ;
