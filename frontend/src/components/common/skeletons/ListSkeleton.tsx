interface ListSkeletonProps {
    count: number;
}

export const ListSkeleton = ({count}: ListSkeletonProps) => {
    const items = Array.from({length: count}, (_, i) => i);

    return (
        <div className="space-y-3" role="status" aria-label="Loading content">
            {items.map((i) => (
                <div key={i} className="flex items-center gap-4 rounded-lg bg-base-100 p-4 shadow">
                    <div className="h-10 w-10 flex-shrink-0 animate-pulse rounded-full bg-base-300"/>
                    <div className="flex-1 space-y-2">
                        <div className="h-4 w-3/4 animate-pulse rounded bg-base-300"/>
                        <div className="h-3 w-1/2 animate-pulse rounded bg-base-300"/>
                    </div>
                    <div className="h-8 w-20 flex-shrink-0 animate-pulse rounded bg-base-300"/>
                </div>
            ))}
            <span className="sr-only">Loading...</span>
        </div>
    );
}
