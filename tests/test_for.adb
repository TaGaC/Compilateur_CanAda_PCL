-- Test de base qui doit foaire;nctionner
with Ada.Text_IO ; use Ada.Text_IO ;
procedure test_for_procedure is
-- VARIABLES
test_for_var : integer ;
I : integer;
-- PROCEDURE PRINCIPALE
begin
  test_for_var := 0;
  for I in 1 .. 5 loop
    test_for_var = 1 ;
  end loop;
end test_for_procedure ; eof
