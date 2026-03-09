export const formatEnum = (status: string): string => {
    if (!status) return "";

    return status
        .toUpperCase()
        .replace(/_/g, " ");
};