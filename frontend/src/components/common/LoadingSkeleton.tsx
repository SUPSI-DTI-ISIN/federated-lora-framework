import {ListSkeleton} from "./skeletons/ListSkeleton";
import {CardSkeleton} from "./skeletons/CardSkeleton";
import {TableSkeleton} from "./skeletons/TableSkeleton";

interface LoadingSkeletonProps {
    variant: "list" | "card" | "table";
    count?: number;
}

export const LoadingSkeleton = ({variant, count = 3}: LoadingSkeletonProps) => {
    if (variant === "list") {
        return <ListSkeleton count={count}/>;
    }

    if (variant === "card") {
        return <CardSkeleton count={count}/>;
    }

    if (variant === "table") {
        return <TableSkeleton count={count}/>;
    }

    return null;
}
