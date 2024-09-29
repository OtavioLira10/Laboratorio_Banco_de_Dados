SELECT * FROM historicos_escolares;
SELECT * FROM turmas;
SELECT * FROM cursos;
SELECT * FROM professores;
SELECT * FROM disciplinas;

SELECT a.cod_curso, a.mgp
FROM alunos a
JOIN cursos c ON a.cod_curso = c.cod_curso;
