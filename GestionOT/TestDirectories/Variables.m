(* Nombres de las variables que se utilizar en las Pruebas *)

Begin["VariablesTest`"];

    (*Multiplataforma, directorio raiz para pruebas unitarias*)
        raizDirectoriosPrueba = FileNameJoin[{$HomeDirectory,
                                        "GIT",
                                        "admin_ot",
                                        "TestDirectories"}];
        
    (*  TEST 3: 
        Directorio vacio, no existen archivos PDF*)

        directorioVacio        = FileNameJoin[{raizDirectoriosPrueba,"1_Empty"}];
    

    
    (*  TEST 4:
        Directorio con una sola carpeta, un grupo de trabajo*)
        directorioUnaCuadrilla = FileNameJoin[{raizDirectoriosPrueba,"2_SingleGroup"}];
        respuestaUnaCuadrilla  = 
            {
                FileNameJoin[{raizDirectoriosPrueba,"2_SingleGroup","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 01-07-2023 (CQ).pdf"}], 
                FileNameJoin[{raizDirectoriosPrueba,"2_SingleGroup","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 02-07-2023 (CQ).pdf"}], 
                FileNameJoin[{raizDirectoriosPrueba,"2_SingleGroup","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 03-07-2023 (CQ).pdf"}], 
                FileNameJoin[{raizDirectoriosPrueba,"2_SingleGroup","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 04-07-2023 (CQ).pdf"}], 
                FileNameJoin[{raizDirectoriosPrueba,"2_SingleGroup","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 05-07-2023 (CQ).pdf"}]
            };

    (*  TEST 5:
        Directorio con una sola carpeta, un grupo de trabajo*)
        directorioUnoErroneo = FileNameJoin[{raizDirectoriosPrueba,"3_SingleWrongPDFs"}];
        respuestaTest4  = 
            {
                FileNameJoin[{raizDirectoriosPrueba,"3_SingleWrongPDFs","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 01-07-2023 (CQ).pdf"}], 
                FileNameJoin[{raizDirectoriosPrueba,"3_SingleWrongPDFs","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 02-07-2023 (CQ).pdf"}], 
                FileNameJoin[{raizDirectoriosPrueba,"3_SingleWrongPDFs","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 03-07-2023 (CQ).pdf"}], 
                FileNameJoin[{raizDirectoriosPrueba,"3_SingleWrongPDFs","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 04-07-2023 (CQ).pdf"}], 
                FileNameJoin[{raizDirectoriosPrueba,"3_SingleWrongPDFs","06 CUADRILLA GUAYZIMI","Orden de trabajo Guayzimi 05-07-2023 (CQ).pdf"}]
            };


End[];