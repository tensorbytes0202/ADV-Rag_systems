import { createContext, useContext, useState } from "react";

const PDFContext = createContext();

export function PDFProvider({ children }) {

    const [pdfState, setPdfState] = useState({

        filename: "",

        page: 1,

        chunk: "",

        parent: ""

    });

    const openPDF = (

        filename,

        page = 1,

        chunk = "",

        parent = ""

    ) => {

        setPdfState({

            filename,

            page,

            chunk,

            parent

        });

    };

    return (

        <PDFContext.Provider

            value={{

                pdfState,

                openPDF

            }}

        >

            {children}

        </PDFContext.Provider>

    );

}

export function usePDF() {

    return useContext(PDFContext);

}