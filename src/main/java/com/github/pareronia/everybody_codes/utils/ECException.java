package com.github.pareronia.everybody_codes.utils;

public class ECException extends RuntimeException {

    private static final long serialVersionUID = 1L;

    public ECException(final String message) {
        super(message);
    }

    public ECException(final Throwable cause) {
        super(cause);
    }
}
